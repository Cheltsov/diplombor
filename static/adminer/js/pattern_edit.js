$(document).ready(function () {

    $('input').attr('autocomplete', 'off');

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

        let count_box = parseInt($('.box-master').last().attr('data-id')) + 1;
        $('.box-master').last().after(`
                <div class="box-master" id="question_box_` + count_box + `" data-id="` + count_box + `">
                    <div class="box">
                        <div class="item">
                            <div style="display: flex; width: 94%; margin-left: 5px;">
                                <input type="text" required class="form-control" autocomplete="off" value="" name="question[` + count_box + `]['title']" placeholder="Введите текст показателя" style="margin-right: 10px;">
                                <button class="btn btn-danger delete_question" data-id="` + count_box + `"><i class="fas fa-trash-alt"></i></button>
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

        if ($('#container_answer_1').children('.box_answer').length != 2) {
            $(this).parent('.box_answer').remove();
        } else {
            alert('Нельзя удалить оценку. Должно быть минимум 2 оценки');
        }
        recalculateAnswer(id_question);
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
                    <input type="text" autocomplete="off" required class="form-control" value="" name="question[` + id_question + `]['answer'][` + count_answer + `]"  placeholder="Введите текст оценки">
                    <input type="number" autocomplete="off" class="form-control" value="" min="0" name="question[` + id_question + `]['sort'][` + count_answer + `]" placeholder="Сорт." style="width: 90px; margin-left: 5px">
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
            $('#container_answer_1').find('.box_answer').each(function () {
                if ($('#question_is_verbal_1').val() == '1') {
                    answers.push({
                        'title': $(this).find('input[type="text"]').val(),
                        'sort': $(this).find('input[type="number"]').val(),
                    });
                } else {
                    answers.push($(this).find('input[type="number"]').val());
                }
            });
            data.push({
                'id': id,
                'title': $(this).find(`input[name="question[` + id + `]['title']"]`).val(),
                'answers': answers,
                'is_verbal': $('#question_is_verbal_1').val()
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
                <input type="number" autocomplete="off" required class="form-control input_number" max="20" style="width: 87%;" name="question[` + id_question + `]['answer'][` + count_answer + `]" placeholder="Введите максильную оценку">
                <span class="cost-answer" id="question[` + id_question + `]['cost'][1]">до 20</span>
                <br>
           </div>`);
            $('#container_answer_' + id_question).parent('.box').css('width', '88%');
            $('#btn_add_answer').removeClass('d-flex');
            $('#btn_add_answer').hide();

        } else {
            $('#container_answer_' + id_question).html(`
            <div class="box_answer" id="box_answer_` + count_answer + `" data-id="1">
                <input type="text" autocomplete="off" required class="form-control" value="" name="question[` + id_question + `]['answer'][1]"  placeholder="Введите текст оценки">
                <input type="number" autocomplete="off" class="form-control" value="" min="0" name="question[` + id_question + `]['sort'][1]" placeholder="Сорт." style="width: 90px; margin-left: 5px">
                <button class="btn btn-danger answer_delete" data-id="1" data-question="` + id_question + `"><i class="fas fa-trash-alt"></i></button>
                <span class="cost-answer" id="question[` + id_question + `]['cost'][1]">0</span>
                <br>
             </div>
             <div class="box_answer" id="box_answer_2" data-id="2">
                <input type="text" autocomplete="off" class="form-control" value="" name="question[` + id_question + `]['answer'][2]" required  placeholder="Введите текст оценки">
                <input type="number" autocomplete="off" class="form-control" value="" min="0" name="question[` + id_question + `]['sort'][2]" placeholder="Сорт." style="width: 90px; margin-left: 5px">
                <button class="btn btn-danger answer_delete" data-id="2" data-question="` + id_question + `"><i class="fas fa-trash-alt"></i></button>
                <span class="cost-answer" id="question[` + id_question + `]['cost'][2]">100</span>
                <br>
             </div>`);
            $('#container_answer_' + id_question).parent('.box').css('width', '100%');
            $('#btn_add_answer').addClass('d-flex');
        }
    });
    // Валидация поле для ввода Числоcлового оценивания
    $(document).on('keydown', '.input_number', function (e) {
        if (e.key.length == 1 && e.key.match(/[^0-9'".]/)) {
            return false;
        }
        if (this.value.length > 1) {
            this.value = this.value.slice(0, 1);
        }
    });

    //Добавление категории
    $('.add_category').click(function (e) {
        e.preventDefault();

        if ($(this).attr('disabled') == 'disabled') {
            return false;
        }

        let json_category = $('#list_category').text();
        let arr_category = JSON.parse(json_category.toString());
        let id_category = parseInt($(this).attr('data-id'));
        let current_category = arr_category.find((el) => {
            return el['id'] === id_category
        });

        //Очистка блока от p
        $('.box-all-category').find('p').hide();

        //Добаление категории в блок
        $('.box-all-category').append(`
            <div class="box-master-category" data-id="` + id_category + `">
                <div class="box-category">
                    <div class="item" style="width: 19%;">
                        <div style="display: flex">
                            <button class="btn btn-danger remove_category" data-id="` + id_category + `"><i class="fas fa-trash-alt"></i></button>
                            <input type="text" autocomplete="off" class="form-control" value="` + current_category['questions'][0]['title'] + `" name="category[` + id_category + `]['title']" disabled>
                        </div>
                    </div>
                    <div class="item" id="container_answer_` + id_category + `"></div>
                </div>
            </div>
        `);

        //Заполнить ответы категории
        current_category['questions'][0]['answers'].forEach(function (el, index) {
            $("#container_answer_" + id_category).append(`
                <div class="box_answer" id="box_answer_` + (index + 1) + `" data-id="` + (index + 1) + `" style="width: 80%;">
                    <input type="text" autocomplete="off" class="form-control" value="` + el['title'] + `" name="category[` + id_category + `]['answer'][` + (index + 1) + `]" disabled>
                    <br>
                </div>
            `);
        });

        $('#btn_add_category_' + id_category).attr('disabled', 'true');
    });

    // Удаление категории
    $(document).on('click', '.remove_category', function (e) {
        e.preventDefault();
        let id_category = parseInt($(this).attr('data-id'));
        $(".box-master-category[data-id='" + id_category + "']").remove();
        $('#btn_add_category_' + id_category).bind("click");

        if ($('.box-master-category').length == 0) {
            $(".box-all-category").html(`<p style="text-align: center">Категории еще не добавлены</p>`);
        }

        $('#btn_add_category_' + id_category).removeAttr('disabled');
    });

});

$(document).ready(function () {

    //Отправить категории
    $('#form_category_edit').submit(function (e) {
        e.preventDefault();
        let data = []
        $(this).find('.box-master').each(function () {
            let id = $(this).attr('data-id');
            let answers = [];
            $(this).find('.box_answer').each(function () {
                answers.push({
                    'title': $(this).find('input[type="text"]').val(),
                    'sort': $(this).find('input[type="number"]').val(),
                });
            });
            data.push({
                'id': id,
                'title': $(this).find(`input[name="question[` + id + `]['title']"]`).val(),
                'answers': answers
            });
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

$(document).ready(function () {
    $('#form_polls_edit').submit(function (e) {
        e.preventDefault();
        let data = []
        $(this).find('.box-master').each(function () {
            let id = $(this).attr('data-id');
            let answers = [];
            $('#container_answer_1').find('.box_answer').each(function () {
                if ($('#question_is_verbal_1').val() == '1') {
                    answers.push({
                        'title': $(this).find('input[type="text"]').val(),
                        'sort': $(this).find('input[type="number"]').val(),
                    });
                } else {
                    answers.push($(this).find('input[type="number"]').val(),);
                }
            });
            data.push({
                'id': id,
                'title': $(this).find(`input[name="question[` + id + `]['title']"]`).val(),
                'answers': answers,
                'is_verbal': $('#question_is_verbal_1').val()
            });
        });

        let data_category = [];
        $(this).find('.box-master-category').each(function () {
            data_category.push($(this).attr('data-id'));
        });

        $.ajax({
            headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val()},
            type: $(this).attr('method'),
            url: $(this).attr('url'),
            dataType: 'json',
            data: {
                'getdata': JSON.stringify(data),
                'polls_title': $('#pattern_title').val(),
                'polls_desc': $('#polls_desc').val(),
                'polls_category': JSON.stringify(data_category),
            },
            success: function (response) {
                console.log(response);
                if (response) {
                    window.location.href = '/admin/polls/';
                }
            }
        })
    });
});

$(document).ready(function () {
    $('.add_pattern').click(function (e) {
        e.preventDefault();
        let id_pattern = $(this).attr('data-id');

        $.ajax({
            type: 'get',
            url: '/admin/pattern/get/' + id_pattern + '/',
            success: function (response) {
                if (response) {
                    renderPattern(response);
                }
            }
        });
    });

    function renderPattern(patterns) {
        pattern = patterns.shift();
        console.log(pattern);

        pattern.questions.forEach(function (el, index) {
            let count_box = parseInt($('.box-master').last().attr('data-id')) + 1;
            $('.box-master').last().after(`
                <div class="box-master" id="question_box_` + count_box + `" data-id="` + count_box + `">
                    <div class="box">
                        <div class="item">
                            <div style="display: flex; width: 94%; margin-left: 5px;">                               
                                <input type="text" autocomplete="off" required class="form-control" value="` + el.title + `" name="question[` + count_box + `]['title']" placeholder="Введите текст показателя" style="margin-right: 10px;">
                                <button class="btn btn-danger delete_question" data-id="` + count_box + `"><i class="fas fa-trash-alt"></i></button>
                            </div>
                        </div>
                    </div>
                </div>`);
        });

        $('.box-master').each(function (){
           if($(this).find('input[type="text"]').val() == '') {
              $(this).remove();
           }
        });

        if (confirm("Хотите перезаписать ответы?")) {
            $('#container_answer_1').find('.box_answer').remove();
            if (pattern.questions[0].is_verbal) {
                $('#question_is_verbal_1').val(1);
                pattern.questions[0].answers.forEach(function (el, index) {
                    $('#container_answer_1').append(`
                        <div class="box_answer" id="box_answer_` + (index) + `" data-id="` + (index) + `">
                            <input type="text" autocomplete="off" class="form-control" value="` + el.title + `" name="question[1]['answer'][` + (index) + `]" required placeholder="Введите текст оценки">
                            <input type="number" autocomplete="off" class="form-control" value="` + el.sort + `" min="0" name="question[1]['sort'][` + (index) + `]" placeholder="Сорт." style="width: 90px; margin-left: 5px">
                            <button class="btn btn-danger answer_delete" data-id="` + (index) + `" data-question="1"><i class="fas fa-trash-alt"></i></button>
                            <span class="cost-answer" id="question[1]['cost'][` + (index) + `]">100</span>
                            <br>
                        </div>`);
                });
                $('#btn_add_answer').addClass('d-flex');
            } else {
                $('#question_is_verbal_1').val(0);
                let answers = pattern.questions[0].answers;
                let length_answers = parseInt(answers.length);
                $('#container_answer_1').append(`
                    <div class="box_answer" id="box_answer_1" data-id="1">
                        <input type="number" autocomplete="off" required class="form-control input_number" max="20" style="width: 87%;" name="question[1]['answer'][1]" placeholder="Введите максильную оценку" value="` + answers[length_answers - 1].title + `">
                        <button class="btn btn-danger answer_delete" data-id="1" data-question="1"><i class="fas fa-trash-alt"></i></button>
                        <span class="cost-answer" id="question[1]['cost'][1]">до 20</span>
                        <br>
                    </div>`);
                $('#btn_add_answer').removeClass('d-flex');
                $('#btn_add_answer').hide();
            }
        }
    }

    function recalculateAnswer(id_container_answer) {
        let arr_cost_answer = $('#container_answer_' + id_container_answer).find('.cost-answer')
        let count_answer = arr_cost_answer.length
        let step = 100 / (parseInt(count_answer) - 1);

        arr_cost_answer.each(function (index) {
            $(this).text(Math.trunc(step * index));
        });
    }

});