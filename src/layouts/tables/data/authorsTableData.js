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

// Material Dashboard 2 React components
import { getFarms } from "api/farmsService";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import MDAvatar from "components/MDAvatar";
import MDBadge from "components/MDBadge";

// Images
import team2 from "assets/images/team-2.jpg";
import team3 from "assets/images/team-3.jpg";
import team4 from "assets/images/team-4.jpg";

export default function data() {
  return {
    columns: [
      { Header: "Cow ID number", accessor: "cow_id", align: "left" },
      { Header: "Date of Birth", accessor: "date_of_birth", align: "left" },
      { Header: "Body Condition Score", accessor: "body_condition_score", align: "center" },
      { Header: "Vaccination Date", accessor: "vaccination_date", align: "left" },
      { Header: "Deworming Date", accessor: "deworming_date", align: "center" },
      // { Header: "Udder health", accessor: "udder_health", align: "center" },
      { Header: "Mastitis", accessor: "mastitis", align: "center" },
      { Header: "Reproductive Health", accessor: "reproductive_health", align: "center" },
      { Header: "Lameness", accessor: "lameness", align: "center" },
      { Header: "General Health", accessor: "general_health", align: "center" },
      // { Header: "Farm Owner", accessor: "owner_name", align: "left" },
    ],
  };
}
