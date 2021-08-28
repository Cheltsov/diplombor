$(document).ready(function () {
    // Удаление вопроса
    $(document).on('click', '.delete_question', function (e) {
        e.preventDefault();
        let id = $(this).attr('data-id');
        if ($('.box').length != 1) {
            $('#question_box_' + id).remove();
        } else {
            alert('Нельзя удалить последний');
        }
    });

    // Добавление вопроса
    $(document).on('click', '#add_question', function (e) {
        e.preventDefault();
        let count_box = parseInt($('#form_pattern_edit').children('.box').last().attr('data-id')) + 1;
        $('.box').last().after(`
                <div class="box" id="question_box_` + count_box + `" data-id="` + count_box + `">
                    <div class="item">
                        <div style="display: flex">
                            <button class="btn btn-danger delete_question" data-id="` + count_box + `"><i class="fas fa-trash-alt"></i></button>
                            <input type="text" required class="form-control" value="" name="question[` + count_box + `]['title']">
                        </div>
                    </div>
                    <div class="item" id="container_answer_` + count_box + `">
                        <div class="box_answer" id="box_answer_1" data-id="1">
                            <input type="text" required class="form-control" value="" name="question[` + count_box + `]['answer'][1]">
                            <button class="btn btn-danger answer_delete" data-id="1" data-question="` + count_box + `"><i class="fas fa-trash-alt"></i></button>
                            <br>
                        </div>
                        <div class="d-flex mt-3" style="width: 87%;">
                            <button class="btn btn-success mx-auto add_answer" data-id="` + count_box + `">Добавить ответ</button>
                        </div>
                    </div>
                </div>`);
    });

    // Удаление ответа
    $(document).on('click', '.answer_delete', function (e) {
        e.preventDefault();
        let id_box_answer = $(this).attr('data-id');
        let id_question = $(this).attr('data-question');

        if ($('#container_answer_' + id_question).children('.box_answer').length != 1) {
            $('#question_box_' + id_question).find('#box_answer_' + id_box_answer).remove();
        } else {
            alert('Нельзя удалить последний');
        }
    });

    // Добавление ответа
    $(document).on('click', '.add_answer', function (e) {
        e.preventDefault();
        let id_question = $(this).attr('data-id');
        let last_answer = $('#container_answer_' + id_question).children('.box_answer').last();
        let count_answer = parseInt(last_answer.attr('data-id')) + 1;

        last_answer.after(`
                <div class="box_answer" id="box_answer_` + count_answer + `" data-id="` + count_answer + `">
                    <input type="text" required class="form-control" value="" name="question[` + id_question + `]['answer'][`+count_answer+`]">
                    <button class="btn btn-danger answer_delete" data-id="` + count_answer + `" data-question="` + id_question + `"><i class="fas fa-trash-alt"></i></button>
                    <br>
                </div>`);
    });

    $('#form_pattern_edit').submit(function (e) {
        e.preventDefault();
        let data = []
        $(this).children('.box').each(function(){
            let id = $(this).attr('data-id');
            let answers = [];
            $(this).find('.box_answer').each(function(){
                answers.push($(this).find('input').val())
            });
            data.push({
                'id': id,
                'title': $(this).find(`input[name="question[`+id+`]['title']"]`).val(),
                'answers': answers
            })
        });
        $.ajax({
            headers: { "X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val() },
            type: $(this).attr('method'),
            url: $(this).attr('url'),
            dataType: 'json',
            data: {'getdata': JSON.stringify(data), 'pattern_title': $('#pattern_title').val()},
            success: function (response){
                console.log(response)
                if(response) {
                    window.location.href = '/admin/pattern/';
                }
            }
        })
    })
});