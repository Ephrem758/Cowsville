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

// Images
import LogoAsana from "assets/images/small-logos/logo-asana.svg";
import logoGithub from "assets/images/small-logos/github.svg";
import logoAtlassian from "assets/images/small-logos/logo-atlassian.svg";
import logoSlack from "assets/images/small-logos/logo-slack.svg";
import logoSpotify from "assets/images/small-logos/logo-spotify.svg";
import logoInvesion from "assets/images/small-logos/logo-invision.svg";

export default function data() {
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
            50
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
            14
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
            35
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
            50
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
            2.0
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
            8
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
            100
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
