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
  // Get H from cow data or default to 6am
  const H = cow?.heat_sign_time
    ? (() => {
        // Check if it's an ISO datetime string
        if (cow.heat_sign_time.includes("T")) {
          return parseInt(cow.heat_sign_time.split("T")[1].split(":")[0], 10);
        }
        // Handle simple time strings (e.g., "06:00")
        return parseInt(cow.heat_sign_time.split(":")[0], 10);
      })()
    : 6;
  const currentTime = new Date().getHours();

  // Generate labels and data
  const labels = [];
  const data = [];
  for (let i = 0; i <= 22; i += 2) {
    const hour = H + 6 + i; // Actual hour (H+6 to H+28)
    const formattedHour = hour % 24; // For display
    labels.push(`${formattedHour.toString().padStart(2, "0")}:00`);

    // Conditions based on ACTUAL HOUR
    if (hour > H + 9 && hour < H + 24) {
      data.push(100); // Green
    } else if (hour >= H + 24 && hour <= H + 28) {
      data.push(50); // Yellow
    } else {
      data.push(50); // Yellow
    }
  }

  // Chart configuration
  const chartData = {
    labels,
    datasets: [
      {
        label: "Probability",
        data,
        segment: {
          borderColor: (ctx) => (ctx.p0.parsed.y === 100 ? "#4CAF50" : "#FFEB3B"),
          backgroundColor: (ctx) => (ctx.p0.parsed.y === 100 ? "#4CAF5030" : "#FFEB3B30"),
        },
        fill: true,
        tension: 0.4,
      },
    ],
  };

  // Pointer logic
  const pointerPosition =
    labels.find((label) => {
      const [hourStr] = label.split(":");
      return parseInt(hourStr, 10) >= currentTime;
    }) || labels[0];

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: {
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
            borderColor: "rgba(255, 255, 255, 0.8)",
            borderWidth: 2,
            label: {
              content: "Now",
              enabled: true,
              position: "top",
            },
          },
        },
      },
    },
    scales: {
      x: { grid: { display: false } },
      y: { min: 0, max: 100, ticks: { stepSize: 50 } },
    },
  };

  return <Line data={chartData} options={chartOptions} />;
};

// ADD PROP-TYPES VALIDATION
SimpleLineChart.propTypes = {
  cow: PropTypes.shape({
    heat_sign_time: PropTypes.string,
  }),
};

export default SimpleLineChart;
