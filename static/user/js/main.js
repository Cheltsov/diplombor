$(document).ready(function () {
    $('.customRange2').each(function () {
        $(this).siblings('.number_range').text(Math.ceil(parseInt($(this).attr('max')) / 2));
    });

    $('.customRange2').change(function () {
        $(this).siblings('.number_range').text($(this).val());
    });

    $('#form_answer').submit(function (e) {
        e.preventDefault();
        let data = [];
        let ip = '';

        $(this).find('select, input[type="range"]').each(function () {
            let id_answer = $(this).val();
            let attr = $(this).attr('data-id-first');
            if(typeof attr !== 'undefined' && attr !== false){
                id_answer = parseInt($(this).attr('data-id-first')) + (parseInt($(this).val() - 1))
            }
            data.push({
                'id_question': $(this).attr('data-question'),
                'id_answer': id_answer,
                'user': ip,
                'is_category': $(this).attr('data-category')
            })
        });

        console.log(data);

        $.ajax({
            headers: {"X-CSRFToken": $('input[name="csrfmiddlewaretoken"]').val()},
            type: $(this).attr('method'),
            url: $(this).attr('url'),
            dataType: 'json',
            data: {
                'getdata': JSON.stringify(data),
            },
            success: function (response) {
                console.log(response);
                if (response == 'true') {
                    alert('Вы прошли опрос');
                }
            }
        });
    });

    function getUserData() {
        var value = $.ajax({
            url: 'http://ipinfo.io',
            async: false,
            dataType: 'json',
        }).responseText;
        return ;
    }

});