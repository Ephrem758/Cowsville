export const calculateDaysDifference = (date1, date2) => {
  const d1 = new Date(date1);
  const d2 = new Date(date2);
  const timeDiff = d2 - d1; // Difference in milliseconds
  return Math.floor(timeDiff / (1000 * 60 * 60 * 24)); // Convert to days
};
