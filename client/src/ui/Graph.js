import { Chart as ChartJS, registerables } from "chart.js";
import { Line, Bar } from "react-chartjs-2";
import "chartjs-adapter-date-fns";
import { enGB } from "date-fns/locale";
//this sets the display language. In the documentation it uses "de", which will display dates in German.
ChartJS.register(...registerables);

function Graph(props) {
  var data = {
    labels: [
      "00:00",
      "01:00",
      "02:00",
      "03:00",
      "04:00",
      "05:00",
      "06:00",
      "07:00",
      "08:00",
      "09:00",
      "10:00",
      "11:00",
      "12:00",
      "13:00",
      "14:00",
      "15:00",
      "16:00",
      "17:00",
      "18:00",
      "19:00",
      "20:00",
      "21:00",
      "22:00",
      "23:00",
    ],
    datasets: [
      {
        fill: "start",
        backgroundColor: function (context, options) {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 380);
          gradient.addColorStop(0, "rgba(210, 43, 43,1)");
          //gradient.addColorStop(0.6, "rgba(253, 218, 13,0.75)");
          gradient.addColorStop(1, "rgba(0, 150, 255,0.5)");
          return gradient;
        },

        borderRadius: 20,
        strokeColor: "#ff6c23",
        pointColor: "#f0f000",
        pointStrokeColor: "#f06c23",
        pointHighlightFill: "#fff000",
        pointHighlightStroke: "#0f6c23",
        data: [
          76351.0, 67379.0, 103254.0, 194757.0, 126079.0, 154091.0, 133017.0,
          111545.0, 150687.0, 119756.0, 117685.0, 134037.0, 133189.0, 119494.0,
          124221.0, 174084.0, 192606.0, 198896.0, 199941.0, 222916.0, 230637.0,
          243008.0, 241194.0, 259011.0,
        ],
      },
    ],
  };
  var options = {
    responsive: true,
    datasetStrokeWidth: 3,
    pointDotStrokeWidth: 4,
    tooltipFillColor: "rgba(0,0,0,0.8)",
    tooltipFontStyle: "bold",
    tooltipTemplate:
      "<%if (label){%><%=label + ' hod' %>: <%}%><%= value + '°C' %>",
    scaleLabel: "<%= Number(value).toFixed(0).replace('.', ',') + '°C'%>",
  };
  return (
    <>
      {props.type == "line" ? (
        <Line options={options} data={data} datasetIdKey='id' />
      ) : (
        <Bar options={options} data={data} datasetIdKey='id' />
      )}
    </>
  );
}

export default Graph;
