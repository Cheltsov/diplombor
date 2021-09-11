$(document).ready(function () {
    // Удаление вопроса
    $(document).on('click', '.delete_question', function (e) {
        e.preventDefault();
        let id = $(this).attr('data-id');
        if ($('.box').length != 1) {
            $('#question_box_' + id).remove();
        } else {
            alert('Нельзя удалить последний вопрос');
        }
    });

    // Добавление вопроса
    $(document).on('click', '#add_question', function (e) {
        e.preventDefault();

        let count_box = parseInt($('#form_pattern_edit').children('.box-master').last().attr('data-id')) + 1;
        $('.box-master').last().after(`
                <div class="box-master" id="question_box_` + count_box + `" data-id="` + count_box + `">
                    <div class="form-group d-flex align-items-center">
                        <label for="question[` + count_box + `]['is_verbal']">Система оценивания вопроса</label>
                        <select id="question[` + count_box + `]['is_verbal']" class="form-control select_verbal" data-id="` + count_box + `" name="question[` + count_box + `]['is_verbal']">
                            <option value="1">Вербальная</option>
                            <option value="0">Числовая</option>
                        </select>
                    </div>
                    <div class="box">
                        <div class="item">
                            <div style="display: flex">
                                <button class="btn btn-danger delete_question" data-id="` + count_box + `"><i class="fas fa-trash-alt"></i></button>
                                <input type="text" required class="form-control" value="" name="question[` + count_box + `]['title']" placeholder="Введите текст вопроса">
                            </div>
                        </div>
                        <div class="item" id="container_answer_` + count_box + `">
                            <div class="box_answer" id="box_answer_1" data-id="1">
                                <input type="text" required class="form-control" value="" name="question[` + count_box + `]['answer'][1]"  placeholder="Введите текст ответа">
                                <button class="btn btn-danger answer_delete" data-id="1" data-question="` + count_box + `"><i class="fas fa-trash-alt"></i></button>
                                <span class="cost-answer" id="question[` + count_box + `]['cost'][1]">0</span>
                                <br>
                            </div>
                            <div class="box_answer" id="box_answer_2" data-id="2">
                                <input type="text" class="form-control" value="" name="question[` + count_box + `]['answer'][2]" required placeholder="Введите текст ответа">
                                <button class="btn btn-danger answer_delete" data-id="2" data-question="` + count_box + `"><i class="fas fa-trash-alt"></i></button>
                                <span class="cost-answer" id="question[` + count_box + `]['cost'][2]">100</span>
                                <br>
                            </div>
                            <div class="d-flex mt-3" style="width: 87%;">
                                <button class="btn btn-success mx-auto add_answer" data-id="` + count_box + `">Добавить ответ</button>
                            </div>
                        </div> 
                    </div>
                </div>`);
    });

    // Удаление ответа
    $(document).on('click', '.answer_delete', function (e) {
        e.preventDefault();
        let id_box_answer = $(this).attr('data-id');
        let id_question = $(this).attr('data-question');

        if ($('#container_answer_' + id_question).children('.box_answer').length != 2) {
            $('#question_box_' + id_question).find('#box_answer_' + id_box_answer).remove();
        } else {
            alert('Нельзя удалить ответ. У вопроса должно быть минимум 2 ответа');
        }
    });

    // Добавление ответа
    $(document).on('click', '.add_answer', function (e) {
        e.preventDefault();
        let id_question = $(this).attr('data-id');
        if ($("#question_is_verbal_" + id_question).val() != 0) {
            addAnswerIsVerbal(id_question);
        }
    });

    function addAnswerIsVerbal(id_question) {
        let last_answer = $('#container_answer_' + id_question).children('.box_answer').last();
        let count_answer = parseInt(last_answer.attr('data-id')) + 1;

        last_answer.after(`
                <div class="box_answer" id="box_answer_` + count_answer + `" data-id="` + count_answer + `">
                    <input type="text" required class="form-control" value="" name="question[` + id_question + `]['answer'][` + count_answer + `]"  placeholder="Введите текст ответа">
                    <button class="btn btn-danger answer_delete" data-id="` + count_answer + `" data-question="` + id_question + `"><i class="fas fa-trash-alt"></i></button>
                    <span class="cost-answer" id="question[` + id_question + `]['cost'][` + count_answer + `]"></span>
                    <br>
                </div>`);

        recalculateAnswer(id_question);
    }

    function recalculateAnswer(id_container_answer) {
        let arr_cost_answer = $('#container_answer_' + id_container_answer).find('.cost-answer')
        let count_answer = arr_cost_answer.length
        let step = 100 / (parseInt(count_answer) - 1);

        arr_cost_answer.each(function (index) {
            $(this).text(Math.trunc(step * index));
        });
    }

    $('#form_pattern_edit').submit(function (e) {
        e.preventDefault();
        let data = []
        $(this).find('.box-master').each(function () {
            let id = $(this).attr('data-id');
            let answers = [];
            $(this).find('.box_answer').each(function () {
                answers.push($(this).find('input').val())
            });
            data.push({
                'id': id,
                'title': $(this).find(`input[name="question[` + id + `]['title']"]`).val(),
                'answers': answers,
                'is_verbal': $(this).find(`select[name="question[` + id + `]['is_verbal']"]`).val()
            })
        });

        $.ajax({
            headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val()},
            type: $(this).attr('method'),
            url: $(this).attr('url'),
            dataType: 'json',
            data: {'getdata': JSON.stringify(data), 'pattern_title': $('#pattern_title').val()},
            success: function (response) {
                console.log(response);
                if (response) {
                    window.location.href = '/admin/pattern/';
                }
            }
        })
    });

    // Изменение системы оценивания
    $(document).on('change', '.select_verbal', function (e) {
        e.preventDefault();

        let id_question = $(this).attr('data-id');
        let count_answer = 1;

        if ($(this).val() == 0) {
            $('#container_answer_' + id_question).html(`
            <div class="box_answer" id="box_answer_` + count_answer + `" data-id="` + count_answer + `">
                <input type="number" required class="form-control input_number" max="100" name="question[` + id_question + `]['answer'][` + count_answer + `]" placeholder="Введите максильную оценку">
                <br>
           </div>`);
            $('#container_answer_' + id_question).parent('.box').css('width', '88%');
        } else {
            $('#container_answer_' + id_question).html(`
            <div class="box_answer" id="box_answer_` + count_answer + `" data-id="1">
                <input type="text" required class="form-control" value="" name="question[` + id_question + `]['answer'][1]"  placeholder="Введите текст ответа">
                <button class="btn btn-danger answer_delete" data-id="1" data-question="` + id_question + `"><i class="fas fa-trash-alt"></i></button>
                <span class="cost-answer" id="question[` + id_question + `]['cost'][1]">0</span>
                <br>
             </div>
             <div class="box_answer" id="box_answer_2" data-id="2">
                <input type="text" class="form-control" value="" name="question[` + id_question + `]['answer'][2]" required  placeholder="Введите текст ответа">
                <button class="btn btn-danger answer_delete" data-id="2" data-question="` + id_question + `"><i class="fas fa-trash-alt"></i></button>
                <span class="cost-answer" id="question[` + id_question + `]['cost'][2]">100</span>
                <br>
             </div>
             <div class="d-flex mt-3" style="width: 87%;">
                <button class="btn btn-success mx-auto add_answer" data-id="` + id_question + `">Добавить ответ</button>
             </div>`);
            $('#container_answer_' + id_question).parent('.box').css('width', '100%');
        }
    });
    // Валидация поле для ввода Числоcлового оценивания
    $(document).on('keydown', '.input_number', function (e) {
        if (e.key.length == 1 && e.key.match(/[^0-9'".]/)) {
            return false;
        }
        if (this.value.length > 2) {
            this.value = this.value.slice(0, 2);
        }
    });
});

$(document).ready(function(){

    //Отправить категории
    $('#form_category_edit').submit(function (e) {
        e.preventDefault();
        let data = []
        $(this).find('.box-master').each(function () {
            let id = $(this).attr('data-id');
            let answers = [];
            $(this).find('.box_answer').each(function () {
                answers.push($(this).find('input').val())
            });
            data.push({
                'id': id,
                'title': $(this).find(`input[name="question[` + id + `]['title']"]`).val(),
                'answers': answers
            })
        });

        $.ajax({
            headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val()},
            type: $(this).attr('method'),
            url: $(this).attr('url'),
            dataType: 'json',
            data: {'getdata': JSON.stringify(data), 'category_title': $('#category_title').val()},
            success: function (response) {
                console.log(response);
                if (response) {
                    window.location.href = '/admin/category/';
                }
            }
        })
    });
});