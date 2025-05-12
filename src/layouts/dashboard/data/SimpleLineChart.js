// SimpleLineChart.js
import React from "react";
import PropTypes from "prop-types";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
} from "chart.js";
import annotationPlugin from "chartjs-plugin-annotation";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, annotationPlugin);

const SimpleLineChart = ({ cow }) => {
  // Safely derive H (hour) from cow.heat_sign_time, with robust type-checking:
  const H = (() => {
    const t = cow?.heat_sign_time;
    if (!t) return 4; // fallback default

    // If it's already a number (0–23), use it
    if (typeof t === "number") {
      return t;
    }

    // If it's a Date object, grab its hour
    if (t instanceof Date) {
      return t.getHours();
    }

    // If it's a string, try parsing it
    if (typeof t === "string") {
      // ISO timestamp?
      if (t.includes("T")) {
        const d = new Date(t);
        // if (!isNaN(d)) return d.getHours();
        if (!isNaN(d)) return d.getUTCHours();
      }
      // HH:mm format?
      const m = t.match(/^(\d{1,2}):\d{2}/);
      if (m) return parseInt(m[1], 10);
    }

    // Last resort
    return 4;
  })();

  const currentTime = new Date().getHours();

  // Build your labels/data exactly as before
  const labels = [];
  const data = [];
  for (let i = 0; i <= 28; i += 2) {
    const hour = H + i;
    // labels.push(`${hour}`);
    labels.push(hour.toString());
    if (i < 6) data.push(10); // Red: 0-6h
    else if (i < 9) data.push(50); // Yellow: 6-9h
    else if (i < 24) data.push(100); // Green: 9-24h
    else if (i <= 28) data.push(50); // Yellow: 24-28h
  }

  const chartData = {
    labels,
    datasets: [
      {
        label: "Probability",
        data,
        segment: {
          borderColor: (ctx) => {
            const y = ctx.p0.parsed.y;
            return y === 100 ? "#4CAF50" : y === 50 ? "#FFEB3B" : "#FF0000";
          },
          backgroundColor: (ctx) => {
            const y = ctx.p0.parsed.y;
            return y === 100 ? "#4CAF5030" : y === 50 ? "#FFEB3B30" : "#FF000030";
          },
        },
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const pointerPosition = labels.find((lbl) => parseInt(lbl, 10) >= currentTime) || labels[0];

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
        mode: "index",
        intersect: false,
        callbacks: {
          label: (ctx) => `Hour: ${ctx.label}, Probability: ${ctx.parsed.y}%`,
        },
      },
      annotation: {
        annotations: {
          currentTime: pointerPosition && {
            type: "line",
            xMin: pointerPosition,
            xMax: pointerPosition,
            borderColor: "rgba(255,255,255,0.8)",
            borderWidth: 2,
            label: { enabled: true, content: "Now", position: "top" },
          },
        },
      },
    },
    scales: {
      x: {
        title: { display: true, text: "Time of Estrus" },
        grid: { display: false },
        ticks: { autoSkip: false, maxRotation: 0, minRotation: 0 },
      },
      y: {
        title: { display: true, text: "Likelihood of pregnancy" },
        min: 0,
        max: 100,
        ticks: { stepSize: 50 },
      },
    },
  };

  return <Line data={chartData} options={chartOptions} />;
};

SimpleLineChart.propTypes = {
  cow: PropTypes.shape({
    heat_sign_time: PropTypes.oneOfType([
      PropTypes.string,
      PropTypes.number,
      PropTypes.instanceOf(Date),
    ]),
  }),
};

export default SimpleLineChart;
