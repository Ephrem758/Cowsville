// OrdersOverview.js
import { useState, useEffect } from "react";
import Card from "@mui/material/Card";
import Icon from "@mui/material/Icon";
import MDBox from "components/MDBox";
import MDTypography from "components/MDTypography";
import TimelineItem from "examples/Timeline/TimelineItem";
import PropTypes from "prop-types";
import { getInseminationRecords } from "api/farmsService";

function OrdersOverview({ cow }) {
  const cowId = cow?.cow_id;
  const farmId = cow?.farm_id ?? cow?.farm?.farm_id;

  // 2) initial count = whatever came from /api/cows/
  const initialCount = Number(cow?.number_of_inseminations) || 0;
  const [inseminationCountState, setInseminationCountState] = useState(initialCount);

  useEffect(() => {
    if (!cowId || !farmId) {
      console.log("Missing cowId or farmId, skipping fetch.");
      return;
    }

    let canceled = false;

    (async () => {
      try {
        // Fetch full array of insemination-records for this cow
        const records = await getInseminationRecords(farmId, cowId);
        console.log("Fetched insemination-records:", records);

        if (canceled) return;

        if (Array.isArray(records) && records.length > 0) {
          const countFromRecords = Number(records[0].insemination_count) || 0;
          console.log("Using countFromRecords:", countFromRecords);
          setInseminationCountState(countFromRecords);
        } else {
          console.log("No records, falling back to initialCount:", initialCount);
          setInseminationCountState(initialCount);
        }
      } catch (err) {
        console.error("Error fetching insemination records:", err);
        setInseminationCountState(initialCount);
      }
    })();

    return () => {
      canceled = true;
    };
  }, [cowId, farmId, initialCount]);

  // Accept cow prop
  return (
    <Card sx={{ height: "100%" }}>
      <MDBox pt={3} px={3}>
        <MDTypography variant="h6" fontWeight="medium">
          Cow Detail: {cow?.cow_id || "N/A"}
        </MDTypography>
        <MDBox mt={0} mb={2}>
          <MDTypography variant="button" color="text" fontWeight="regular">
            <MDTypography display="inline" variant="body2" verticalAlign="middle">
              <Icon sx={{ color: ({ palette: { success } }) => success.main }}>arrow_upward</Icon>
            </MDTypography>
            &nbsp;
            <MDTypography variant="button" color="text" fontWeight="medium">
              {inseminationCountState} inseminations
              {/* {cow?.number_of_inseminations || "0"} inseminations */}
            </MDTypography>{" "}
            so far
          </MDTypography>
        </MDBox>
      </MDBox>
      <MDBox p={2}>
        <TimelineItem
          color="success"
          icon="notifications"
          title="Heat Signs"
          description={cow?.heat_signs || "N/A"}
        />
        <TimelineItem
          color="error"
          icon="inventory_2"
          title="Calving Date"
          description={cow?.calving_date || "N/A"}
        />
        <TimelineItem
          color="info"
          icon="shopping_cart"
          title="Date of AI"
          description={cow?.last_date_insemination || "N/A"}
        />
        <TimelineItem
          color="warning"
          icon="payment"
          title="Average milk yield (L)"
          description={cow?.average_daily_milk || "N/A"}
        />
        <TimelineItem
          color="primary"
          icon="pets"
          title="Breed"
          description={cow?.breed_name || "N/A"}
          lastItem
        />
      </MDBox>
    </Card>
  );
}

// Add prop validation
OrdersOverview.propTypes = {
  cow: PropTypes.shape({
    cow_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    farm_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    farm: PropTypes.shape({
      farm_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    }),
    heat_signs: PropTypes.string,
    calving_date: PropTypes.string,
    last_date_insemination: PropTypes.string,
    number_of_inseminations: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    lactation_number: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    breed_name: PropTypes.string,
    average_daily_milk: PropTypes.string,
    insemination_count: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  }),
};

export default OrdersOverview;
