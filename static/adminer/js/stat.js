$(document).ready(function () {

    sendAjax();

    $('.select_category_btn').click(function () {
        sendAjax();
        alert('Поиск завершен');
    });
    // Запрос на получение статистики
    function sendAjax() {
        $.ajax({
            headers: {"X-CSRFToken": $('#csrfmiddlewaretoken').text()},
            type: 'post',
            url: '/admin/polls/stat_ajax/' + $('.h_poll').attr('data-id') + '/',
            dataType: 'json',
            data: {'id_category': $('.select_category').val()},
            success: function (response) {
                console.log(response)
                $("#chart_div").empty();
                $('.tr_question').remove();
                $('.renderChartRemove').remove();
                if (response) {
                    if (response.word == "Недостаточно экспертов") {
                        alert('Недостаточно экспертов');
                    }
                    renderTableS(response.list_q_mark);
                    renderSircleChart(response.list_q_mark);
                    $('.math4').text(response.word);
                    $('.math5').text(response.coord);
                    renderCountMark(response.count_mark, response.list_q_mark)
                }
            }
        });
    }
    // Отобразить таблицу параметров S!, S6, Sch
    function renderTableS(list_q_mark) {
        $('.tr_question').remove();
        list_q_mark.forEach(function (item, index) {
            $('.tableS').find('tbody').append(`
                <tr class="tr_question">
                    <td class="title_question">` + item.question_title + `</td>
                    <td class="s1">` + item.s1 + `</td>
                    <td class="s6">` + item.s6 + `</td>
                    <td class="sch">` + (item.sch == 0 ? 'Недостаточно экспертов' :  item.sch) + `</td>
                </tr>`);
        });
    }
    // Отобразить круглый график
    function renderSircleChart(list_q_mark) {

        $('#chart_div').css('height', (50 * parseInt(list_q_mark.length))+'px');

        google.charts.load('current', {packages: ['corechart', 'bar']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            let data_to_tabel = [['Показатель', 'S1', 'S2', 'S3']];
            list_q_mark.forEach(function (item, index) {
                let i = index+1
                //$('.legend_question').append("<p>"+ i + " - "+ item.question_title +"</p>")
                data_to_tabel.push([item.question_title, item.s1, item.s6, item.sch]);
            });

            let data = google.visualization.arrayToDataTable(data_to_tabel);

            let options = {
                chart: {
                    title: 'Столбчатая диаграмма',
                },
                orientation: 'vertical'
            };

            let chart = new google.charts.Bar(document.getElementById('chart_div'));
            chart.draw(data, google.charts.Bar.convertOptions(options));
        }
    }
    // отобразить кол-во оценкок каждого показателя
    function renderCountMark(list_count_mark, list_q_mark) {
        $('.renderChartRemove').remove();
        list_count_mark.forEach(function (item, index) {
            $('.head-form').last().after(`
                <div class="head-form renderChartRemove">
                    <div>
                        <h3>Оценки по показателю "` + list_q_mark[index]['question_title'] + `"</h3>
                        <div style="margin-top: 20px; margin-left: 10px; display: none" class="other_list_block` + (index) + `">
                            <h5>Дополнительные ответы пользователей:</h5>
                            <ul class="other_list` + (index) + `">
                            </ul>
                        </div>
                    </div>
                    <div id="piechart` + (index) + `" style="width: 100%; height: 500px;"></div>
                    <br>
                </div>`);

                let list_other = JSON.parse(list_q_mark[index]['other_answer']);
                if(list_other.length > 0) {
                    $(".other_list_block"+index).show();
                    list_other.forEach(function(item){
                        $(".other_list"+index).append("<li>" + item[0] + "</li>")
                    });
                }


            let data_chart = [];
            data_chart.push(['Task', 'Hours per Day']);

            for (const [key, value] of Object.entries(item)) {
                data_chart.push(['Оценка: '+key, value]);
            }

            smallRenderCountMark('Ответы по показателю "' + list_q_mark[index]['question_title'] + '"', 'piechart' + index, data_chart)
        });
    }
    // Круговой график для каждого показателя
    function smallRenderCountMark(title_chart, id_div, data_chart) {
        google.charts.load('current', {'packages': ['corechart']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            var data = google.visualization.arrayToDataTable(data_chart);
            var options = {
                title: title_chart,
                is3D: true,
            };
            var chart = new google.visualization.PieChart(document.getElementById(id_div));
            chart.draw(data, options);
        }
    }

    $('#print_pdf').click(function (e) {
        e.preventDefault();
        $.ajax({
            headers: {"X-CSRFToken": $('#csrfmiddlewaretoken').text()},
            type: 'post',
            url: '/admin/polls/create_pdf/' + $('.h_poll').attr('data-id') + '/',
            data: {'id_category': $('.select_category').val()},
            dataType: 'json',
            success: function (response) {
                 window.open(response);
            }
        });
    });

    $('#refresh_report').click(function(){
        alert('Выполняется обновление')
        $.ajax({
            headers: {"X-CSRFToken": $('#csrfmiddlewaretoken').text()},
            type: 'post',
            url: '/admin/polls/refresh_stat_ajax/' + $('.h_poll').attr('data-id') + '/',
            success: function (response) {
                 if(response == 'true') {
                     window.location.reload();
                 } else {
                     alert('Ошибка')
                 }
            }
        });
    });
});