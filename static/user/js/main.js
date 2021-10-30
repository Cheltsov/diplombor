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
        let date = new Date();
        let id_user =  date.getFullYear().toString() + date.getMonth().toString() + date.getDate().toString() + date.getHours().toString() + date.getMinutes().toString() + date.getSeconds().toString();

        $(this).find('select, input[type="range"]').each(function () {
            let id_answer = $(this).val();
            let attr = $(this).attr('data-id-first');
            if(typeof attr !== 'undefined' && attr !== false){
                id_answer = parseInt($(this).attr('data-id-first')) + (parseInt($(this).val() - 1))
            }

            let id_category = 0;
            if($('select[data-is-category="1"]').length > 0){
                id_category = $('select[data-is-category="1"]').val();
            }
            data.push({
                'id_question': parseInt($(this).attr('data-question')),
                'id_answer': id_answer,
                'user': id_user,
                'is_category': $(this).attr('data-is-category'),
                'id_category': id_category
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
                window.location.href="/user/thank/";
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