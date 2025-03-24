/**
=========================================================
* Material Dashboard 2 React - v2.2.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/

// export default {
//   sales: {
//     labels: ["4pm", "6pm", "8pm", "10pm", "12am", "2am", "4am", "6am", "8am"],
//     datasets: { label: "Mobile apps", data: [50, 40, 300, 320, 500, 350, 200, 230, 500] },
//   },
//   tasks: {
//     labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
//     datasets: { label: "Desktop apps", data: [50, 40, 300, 220, 500, 250, 400, 230, 500] },
//   },
// };
// ReportsLineChart.js;
// ReportsLineChart.js (Original Version)
// ReportsLineChart.js (Dynamic Version)
import React from "react";
import { Line } from "react-chartjs-2";
import MDTypography from "components/MDTypography";
import MDBox from "components/MDBox";
import Card from "@mui/material/Card";
import PropTypes from "prop-types";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip);

function ReportsLineChart({ cow }) {
  // Hardcoded static data (for testing)
  const H = cow?.heat_sign_time || "06:00";
  const heatHour = parseInt(H.split(":")[0], 10) || 6;

  const labels = [];
  for (let i = 0; i <= 22; i += 2) {
    const hour = heatHour + 6 + i;
    labels.push(`${(hour % 24).toString().padStart(2, "0")}:00`);
  }

  const data = labels.map((_, index) => {
    const currentHour = heatHour + 6 + index * 2;
    if (currentHour >= heatHour + 9 && currentHour < heatHour + 24) return 100;
    if (currentHour >= heatHour + 24 && currentHour <= heatHour + 28) return 50;
    return 0;
  });

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Probability",
        data: data,
        borderColor: "#4CAF50",
        backgroundColor: "#4CAF5030",
        fill: true,
        tension: 0.4,
      },
    ],
  };

  return (
    <Card>
      <MDBox p={2}>
        <Line data={chartData} />
        {!cow && (
          <MDTypography variant="caption" color="warning" textAlign="center">
            Using default heat sign time (6am)
          </MDTypography>
        )}
      </MDBox>
    </Card>
  );
}

ReportsLineChart.propTypes = { cow: PropTypes.object };
ReportsLineChart.defaultProps = { cow: null };

export default ReportsLineChart;
