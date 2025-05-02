import { calculateDaysDifference } from "utils/helpers";
import PropTypes from "prop-types"; // Import PropTypes
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDAvatar from "components/MDAvatar";
import MDProgress from "components/MDProgress";
import Icon from "@mui/material/Icon";
import LogoAsana from "assets/images/small-logos/logo-asana.svg";

// Define Project component
const Project = ({ image, name }) => (
  <MDBox display="flex" alignItems="center" lineHeight={1}>
    <MDAvatar src={image} name={name} size="sm" variant="rounded" />
    <MDTypography display="block" variant="button" fontWeight="medium" ml={1} lineHeight={1}>
      {name}
    </MDTypography>
  </MDBox>
);

Project.propTypes = {
  image: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
};

// Define Progress component
const Progress = ({ color, value }) => (
  <MDBox display="flex" alignItems="center">
    <MDTypography variant="caption" color="text" fontWeight="medium">
      {value}%
    </MDTypography>
    <MDBox ml={0.5} width="9rem">
      <MDProgress variant="gradient" color={color} value={value} />
    </MDBox>
  </MDBox>
);

Progress.propTypes = {
  color: PropTypes.string.isRequired,
  value: PropTypes.number.isRequired,
};

export default function averageStatisticsData(allCows = []) {
  if (!Array.isArray(allCows) || allCows.length === 0) {
    console.warn("No cows available for calculations.");
    return {
      columns: [],
      rows: [],
    };
  }

  // Calculate metrics for all cows
  const calculateAverageInseminationAfterCalving = (cows) => {
    if (!cows || cows.length === 0) return 0;
    const validCows = cows.filter(
      (cow) => cow.calving_date !== "N/A" && cow.recent_insemination_date !== "N/A"
    );
    if (validCows.length === 0) return 0;
    const totalDays = validCows.reduce((sum, cow) => {
      const days = calculateDaysDifference(cow.calving_date, cow.recent_insemination_date);
      return sum + days;
    }, 0);
    return totalDays / validCows.length;
  };
  const averageInseminationAfterCalving = calculateAverageInseminationAfterCalving(allCows);

  const calculateAverageCalvingInterval = (cows) => {
    if (!cows || cows.length === 0) return 0;
    const validCows = cows.filter(
      (cow) => cow.calving_date !== "N/A" && cow.last_calving_date !== "N/A"
    );
    if (validCows.length === 0) return 0;
    const totalMonths = validCows.reduce((sum, cow) => {
      const months = calculateDaysDifference(cow.last_calving_date, cow.calving_date) / 30;
      return sum + months;
    }, 0);
    return totalMonths / validCows.length;
  };
  const averageCalvingInterval = calculateAverageCalvingInterval(allCows);

  const calculateAverageHeatAfterCalving = (cows) => {
    if (!cows || cows.length === 0) return 0;
    const validCows = cows.filter(
      (cow) => cow.calving_date !== "N/A" && cow.heat_sign_date !== "N/A"
    );
    if (validCows.length === 0) return 0;
    const totalDays = validCows.reduce((sum, cow) => {
      const days = calculateDaysDifference(cow.calving_date, cow.heat_sign_date);
      return sum + days;
    }, 0);
    return totalDays / validCows.length;
  };
  const averageHeatAfterCalving = calculateAverageHeatAfterCalving(allCows);

  const calculateCowsReturnToHeatWithin60Days = (cows) => {
    if (!cows || cows.length === 0) return 0;
    const validCows = cows.filter(
      (cow) => cow.calving_date !== "N/A" && cow.heat_sign_date !== "N/A"
    );
    if (validCows.length === 0) return 0;
    const eligibleCows = validCows.filter((cow) => {
      const days = calculateDaysDifference(cow.calving_date, cow.heat_sign_date);
      return days <= 60;
    });
    return (eligibleCows.length / validCows.length) * 100 || 0;
  };
  const cowsReturnToHeatWithin60Days = calculateCowsReturnToHeatWithin60Days(allCows);

  const calculateAverageServicesPerConception = (cows) => {
    if (!cows || cows.length === 0) return 0;
    const validCows = cows.filter((cow) => cow.insemination_count !== "N/A");
    if (validCows.length === 0) return 0;
    const totalServices = validCows.reduce((sum, cow) => sum + cow.insemination_count, 0);
    return totalServices / validCows.length || 0;
  };
  const averageServicesPerConception = calculateAverageServicesPerConception(allCows);

  const calculateRateOfMatureCowsDoing3Services = (cows) => {
    if (!cows || cows.length === 0) return 0;
    const validCows = cows.filter((cow) => cow.insemination_count !== "N/A");
    if (validCows.length === 0) return 0;
    const matureCows = validCows.filter((cow) => cow.insemination_count > 3);
    return (matureCows.length / validCows.length) * 100 || 0;
  };

  const rateOfMatureCowsDoing3Services = calculateRateOfMatureCowsDoing3Services(allCows);

  const calculateRateOfCowsWithIntervalBetweenCalvingAndPregnancy = (cows) => {
    if (!cows || cows.length === 0) return 0;
    const validCows = cows.filter((cow) => cow.calving_date !== "N/A");
    if (validCows.length === 0) return 0;
    const eligibleCows = validCows.filter((cow) => {
      if (!cow.is_pregnant) {
        const monthsSinceCalving = calculateDaysDifference(cow.calving_date, new Date()) / 30;
        return monthsSinceCalving >= 3;
      } else {
        if (cow.pregnancy_date === "N/A") return false;
        const monthsSinceCalving =
          calculateDaysDifference(cow.calving_date, cow.pregnancy_date) / 30;
        return monthsSinceCalving >= 3;
      }
    });
    return (eligibleCows.length / validCows.length) * 100 || 0;
  };
  const rateOfCowsWithIntervalBetweenCalvingAndPregnancy =
    calculateRateOfCowsWithIntervalBetweenCalvingAndPregnancy(allCows);

  return {
    columns: [
      { Header: "Indicator", accessor: "indicator", width: "30%", align: "left" },
      { Header: "Value", accessor: "value", align: "left" },
      { Header: "Unit", accessor: "unit", align: "center" },
      { Header: "Goal", accessor: "goal", align: "center" },
      { Header: "Action", accessor: "action", align: "center" },
    ],
    rows: [
      {
        indicator: <Project image={LogoAsana} name="Insemination after calving" />,
        value: (
          <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
            {averageInseminationAfterCalving.toFixed(2)}
          </MDTypography>
        ),
        unit: (
          <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
            Days
          </MDTypography>
        ),
        goal: <Progress color="info" value={60} />,
        action: (
          <MDTypography component="a" href="#" color="text">
            <Icon>more_vert</Icon>
          </MDTypography>
        ),
      },
      {
        indicator: <Project image={LogoAsana} name="Average Calving interval" />,
        value: (
          <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
            {averageCalvingInterval.toFixed(2)}
          </MDTypography>
        ),
        unit: (
          <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
            Months
          </MDTypography>
        ),
        goal: <Progress color="success" value={100} />,
        action: (
          <MDTypography component="a" href="#" color="text">
            <Icon>more_vert</Icon>
          </MDTypography>
        ),
      },
      {
        indicator: <Project image={LogoAsana} name="Heat after calving" />,
        value: (
          <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
            {averageHeatAfterCalving.toFixed(2)}
          </MDTypography>
        ),
        unit: (
          <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
            Days
          </MDTypography>
        ),
        goal: <Progress color="error" value={30} />,
        action: (
          <MDTypography component="a" href="#" color="text">
            <Icon>more_vert</Icon>
          </MDTypography>
        ),
      },
      // {
      //   indicator: <Project image={LogoAsana} name="Cows return to heat within 60 days" />,
      //   value: (
      //     <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
      //       {cowsReturnToHeatWithin60Days.toFixed(2)}
      //     </MDTypography>
      //   ),
      //   unit: (
      //     <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
      //       %
      //     </MDTypography>
      //   ),
      //   goal: <Progress color="info" value={80} />,
      //   action: (
      //     <MDTypography component="a" href="#" color="text">
      //       <Icon>more_vert</Icon>
      //     </MDTypography>
      //   ),
      // },
      {
        indicator: <Project image={LogoAsana} name="No. of inseminations per conception" />,
        value: (
          <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
            {averageServicesPerConception.toFixed(2)}
          </MDTypography>
        ),
        unit: (
          <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
            Number
          </MDTypography>
        ),
        goal: <Progress color="error" value={0} />,
        action: (
          <MDTypography component="a" href="#" color="text">
            <Icon>more_vert</Icon>
          </MDTypography>
        ),
      },
      {
        indicator: <Project image={LogoAsana} name="Rate of mature cows doing 03 services" />,
        value: (
          <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
            {rateOfMatureCowsDoing3Services.toFixed(2)}
          </MDTypography>
        ),
        unit: (
          <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
            %
          </MDTypography>
        ),
        goal: <Progress color="success" value={100} />,
        action: (
          <MDTypography component="a" href="#" color="text">
            <Icon>more_vert</Icon>
          </MDTypography>
        ),
      },
      {
        indicator: (
          <Project
            image={LogoAsana}
            name="Rate of cows with interval between calving and pregnancy"
          />
        ),
        value: (
          <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
            {rateOfCowsWithIntervalBetweenCalvingAndPregnancy.toFixed(2)}
          </MDTypography>
        ),
        unit: (
          <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
            %
          </MDTypography>
        ),
        goal: <Progress color="success" value={100} />,
        action: (
          <MDTypography component="a" href="#" color="text">
            <Icon>more_vert</Icon>
          </MDTypography>
        ),
      },
    ],
  };
}
