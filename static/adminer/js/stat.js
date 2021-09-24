$(document).ready(function () {

    sendAjax();

    $('.select_category').change(function () {
        sendAjax();
    });

    function sendAjax() {
        $.ajax({
            headers: {"X-CSRFToken": $('#csrfmiddlewaretoken').text()},
            type: 'post',
            url: '/admin/polls/stat_ajax/' + $('.h_poll').attr('data-id') + '/',
            dataType: 'json',
            data: {'id_category': $('.select_category').val()},
            success: function (response) {
                if (response) {
                    renderTableS(response.list_q_mark);
                    renderSircleChart(response.list_q_mark);
                    $('.math4').text(response.word);
                    $('.math5').text(response.coord);
                    renderCountMark(response.count_mark)
                }
            }
        });
    }

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

    function renderSircleChart(list_q_mark) {
        google.charts.load('current', {packages: ['corechart', 'bar']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {
            let data_to_tabel = [['Показатель', 'S1', 'S2', 'S3']];
            list_q_mark.forEach(function (item, index) {
                data_to_tabel.push([item.question_title, item.s1, item.s6, item.sch]);
            });

            let data = google.visualization.arrayToDataTable(data_to_tabel);

            let options = {
                chart: {
                    title: 'Столбчатая диаграмма',
                }
            };

            let chart = new google.charts.Bar(document.getElementById('chart_div'));
            chart.draw(data, google.charts.Bar.convertOptions(options));
        }
    }

    function renderCountMark(list_count_mark) {
        $('.renderChartRemove').remove();
        list_count_mark.forEach(function (item, index) {

            $('.head-form').last().after(`
                <div class="head-form renderChartRemove">
                    <h3>Оценки по показателю ` + (index + 1) + `</h3>
                    <div id="piechart` + (index) + `" style="width: 100%; height: 500px;"></div>
                    <br>
                </div>`);

            let data_chart = [];
            data_chart.push(['Task', 'Hours per Day']);

            for (const [key, value] of Object.entries(item)) {
                data_chart.push(['Оценка: '+key, value]);
            }

            smallRenderCountMark('Ответы по показателю ' + (index + 1), 'piechart' + index, data_chart)
        });
    }

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


});