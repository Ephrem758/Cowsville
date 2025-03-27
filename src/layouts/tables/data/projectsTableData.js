/* eslint-disable react/prop-types */
/* eslint-disable react/function-component-definition */
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

// @mui material components
import Icon from "@mui/material/Icon";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDAvatar from "components/MDAvatar";
import MDProgress from "components/MDProgress";
import { calculateDaysDifference } from "utils/helpers";

// Images
import LogoAsana from "assets/images/small-logos/logo-asana.svg";
import logoGithub from "assets/images/small-logos/github.svg";
import logoAtlassian from "assets/images/small-logos/logo-atlassian.svg";
import logoSlack from "assets/images/small-logos/logo-slack.svg";
import logoSpotify from "assets/images/small-logos/logo-spotify.svg";
import logoInvesion from "assets/images/small-logos/logo-invision.svg";

export default function data(searchedFarmId = null, mockCows = []) {
  const Project = ({ image, name }) => (
    <MDBox display="flex" alignItems="center" lineHeight={1}>
      <MDAvatar src={image} name={name} size="sm" variant="rounded" />
      <MDTypography display="block" variant="button" fontWeight="medium" ml={1} lineHeight={1}>
        {name}
      </MDTypography>
    </MDBox>
  );

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

  // Filter cows by searched farm ID
  const filteredCows = searchedFarmId
    ? mockCows.filter((cow) => cow.farm_id === searchedFarmId)
    : [];

  // Calculate average insemination after calving
  const calculateAverageInseminationAfterCalving = (cows) => {
    if (!Array.isArray(cows) || cows.length === 0) return 0;

    const totalDays = cows.reduce((sum, cow) => {
      const days = calculateDaysDifference(cow.calving_date, cow.recent_insemination_date);
      return sum + days;
    }, 0);
    return totalDays / cows.length;
  };

  const averageInseminationAfterCalving = calculateAverageInseminationAfterCalving(filteredCows);

  // Average Calving Interval
  const calculateAverageCalvingInterval = (cows) => {
    if (!Array.isArray(cows) || cows.length === 0) return 0;

    const totalMonths = cows.reduce((sum, cow) => {
      const months = calculateDaysDifference(cow.last_calving_date, cow.calving_date) / 30; // Approximate months
      return sum + months;
    }, 0);

    return totalMonths / cows.length;
  };

  const averageCalvingInterval = calculateAverageCalvingInterval(filteredCows);

  // Heat after calving
  const calculateAverageHeatAfterCalving = (cows) => {
    if (!Array.isArray(cows) || cows.length === 0) return 0;

    const totalDays = cows.reduce((sum, cow) => {
      const days = calculateDaysDifference(cow.calving_date, cow.heat_sign_date);
      return sum + days;
    }, 0);

    return totalDays / cows.length;
  };

  const averageHeatAfterCalving = calculateAverageHeatAfterCalving(filteredCows);

  // Cows return to heat within 60 days
  const calculateCowsReturnToHeatWithin60Days = (cows) => {
    if (!Array.isArray(cows) || cows.length === 0) return 0;

    const eligibleCows = cows.filter((cow) => {
      const days = calculateDaysDifference(cow.calving_date, cow.heat_sign_date);
      return days <= 60;
    });

    return (eligibleCows.length / cows.length) * 100 || 0;
  };

  const cowsReturnToHeatWithin60Days = calculateCowsReturnToHeatWithin60Days(filteredCows);

  // No. of services per conception
  const calculateAverageServicesPerConception = (cows) => {
    if (!Array.isArray(cows) || cows.length === 0) return 0;

    const totalServices = cows.reduce((sum, cow) => sum + cow.insemination_count, 0);

    return totalServices / cows.length;
  };

  const averageServicesPerConception = calculateAverageServicesPerConception(filteredCows);

  // Rate of mature cows doing 03 services
  const calculateRateOfMatureCowsDoing3Services = (cows) => {
    if (!Array.isArray(cows) || cows.length === 0) return 0;

    const matureCows = cows.filter((cow) => cow.insemination_count > 3);

    return (matureCows.length / cows.length) * 100 || 0;
  };

  const rateOfMatureCowsDoing3Services = calculateRateOfMatureCowsDoing3Services(filteredCows);

  // Rate of cows with interval between calving and pregnancy
  const calculateRateOfCowsWithIntervalBetweenCalvingAndPregnancy = (cows) => {
    if (!Array.isArray(cows) || cows.length === 0) return 0;

    const eligibleCows = cows.filter((cow) => {
      if (!cow.pregnancy_status) {
        // For not pregnant cows: Check time since calving
        const monthsSinceCalving = calculateDaysDifference(cow.calving_date, new Date()) / 30; // Approximate months
        return monthsSinceCalving >= 3;
      } else {
        // For pregnant cows: Check time between calving and pregnancy
        const monthsSinceCalving =
          calculateDaysDifference(cow.calving_date, cow.pregnancy_date) / 30; // Approximate months
        return monthsSinceCalving >= 3;
      }
    });

    return (eligibleCows.length / cows.length) * 100 || 0;
  };

  const rateOfCowsWithIntervalBetweenCalvingAndPregnancy =
    calculateRateOfCowsWithIntervalBetweenCalvingAndPregnancy(filteredCows);

  return {
    columns: [
      { Header: "Indicator", accessor: "indicator", width: "30%", align: "left" },
      { Header: "Value", accessor: "value", align: "left" },
      { Header: "Unit", accessor: "unit", align: "center" },
      { Header: "Goal", accessor: "goal", align: "center" },
      { Header: "action", accessor: "action", align: "center" },
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
      {
        indicator: <Project image={LogoAsana} name="Cows return to heat within 60 days" />,
        value: (
          <MDTypography component="a" href="#" variant="button" color="text" fontWeight="medium">
            {cowsReturnToHeatWithin60Days.toFixed(2)}
          </MDTypography>
        ),
        unit: (
          <MDTypography component="a" href="#" variant="caption" color="text" fontWeight="medium">
            %
          </MDTypography>
        ),
        goal: <Progress color="info" value={80} />,
        action: (
          <MDTypography component="a" href="#" color="text">
            <Icon>more_vert</Icon>
          </MDTypography>
        ),
      },
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
