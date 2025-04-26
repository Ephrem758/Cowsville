// FarmCards.js
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // For navigation
import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import Footer from "examples/Footer";
import { getFarms, getCows } from "api/farmsService"; // Import API function
import mockFarms from "./mockFarms";
import { mockCows } from "layouts/tables/";

function FarmCards() {
  const navigate = useNavigate();
  const [farms, setFarms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // Hardcoded farms (replace with API data later)

  const farmImageMapping = {
    28: "/images/farm-cards/image-1.jpg",
    31: "/images/farm-cards/image-3.jpg",
    24: "/images/farm-cards/image-4.jpg",
    12: "/images/farm-cards/image-5.jpg",
    9: "/images/farm-cards/image-6.jpg",
    4: "/images/farm-cards/image-2.jpg",
    FARM001: "/images/farm-cards/image-2.jpg",
    1: "/images/farm-cards/image-2.jpg",
    3: "/images/farm-cards/image-2.jpg",
    // Add more mappings as needed
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Fetch backend farms and cows
        const [farmsResponse, cowsResponse] = await Promise.all([getFarms(), getCows()]);
        const backendFarms = Array.isArray(farmsResponse)
          ? farmsResponse
          : farmsResponse.farms || [];
        const allCows = Array.isArray(cowsResponse) ? cowsResponse : cowsResponse.cows || [];

        console.log("All Cows Data:", allCows); // Debugging cows data

        // Calculate total cows per farm using cow.farm_id
        const backendFarmCowCounts = allCows.reduce((acc, cow) => {
          if (cow.farm_id) {
            acc[cow.farm_id] = (acc[cow.farm_id] || 0) + 1;
          }
          return acc;
        }, {});

        console.log("Cow Counts:", backendFarmCowCounts); // Debugging cow counts

        // Merge backend farms with calculated totals using farm.farm_id as the key
        const mergedFarms = backendFarms.map((farm) => ({
          ...farm,
          totalCows: backendFarmCowCounts[farm.farm_id] || 0,
          image: farm.image || "/images/farm-cards/default-image.jpg",
        }));

        console.log("Backend Farms:", mergedFarms); // Debugging backend farms

        // Use only backend data (no mock data)
        setFarms(mergedFarms);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <DashboardLayout>
      <DashboardNavbar />
      <MDBox pt={6} pb={3}>
        <Grid container spacing={3}>
          {farms.map((farm) => (
            <Grid item xs={12} md={6} lg={4} key={farm.id}>
              <Card
                sx={{
                  cursor: "pointer",
                  transition: "transform 0.2s",
                  "&:hover": { transform: "scale(1.05)" },
                }}
                onClick={() => navigate(`/tables?farm_id=${farm.farm_id}`)} // Add later
              >
                <MDBox p={3} textAlign="center">
                  <MDBox
                    component="img"
                    // src="/images/farm-cards/image-2.jpg"
                    src={farmImageMapping[farm.farm_id] || "/images/farm-cards/default-image.jpg"} // Use mapping
                    alt={farm.name}
                    onError={(e) => {
                      e.target.src = "/images/farm-cards/fallback-image.jpg"; // Fallback
                    }}
                    width="80%"
                    height="150px"
                    mx="auto"
                    borderRadius="md"
                    mb={2}
                  />
                  <MDTypography variant="h4" fontWeight="bold" color="info" mb={1}>
                    {farm.owner_name} Farm
                  </MDTypography>

                  <MDBox display="flex" alignItems="center" justifyContent="center" mt={1} mb={1.5}>
                    <MDTypography
                      variant="button"
                      color="text"
                      fontWeight="medium"
                      mr={1}
                      sx={{ minWidth: "90px", textAlign: "right" }} // Set min width
                    >
                      Farm ID :
                    </MDTypography>
                    <MDTypography variant="h6" fontWeight="medium" color="info">
                      {farm.farm_id}
                    </MDTypography>
                  </MDBox>

                  {/* Total Cows */}
                  <MDBox display="flex" alignItems="center" justifyContent="center" mb={1}>
                    <MDTypography
                      variant="button"
                      color="text"
                      fontWeight="medium"
                      mr={1}
                      sx={{ minWidth: "80px", textAlign: "right" }} // Set the same min width
                    >
                      Total Cows :
                    </MDTypography>
                    <MDTypography variant="h6" fontWeight="medium" color="info">
                      {/* {farm.totalCows} */}
                      {farm.total_number_of_cows}
                    </MDTypography>
                  </MDBox>
                </MDBox>
              </Card>
            </Grid>
          ))}
        </Grid>
      </MDBox>
      <Footer />
    </DashboardLayout>
  );
}

export default FarmCards;
