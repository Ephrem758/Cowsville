// Mock clusters and farm membership
// Each cluster lists the farm_ids that belong to it. Cows already carry farm_id.

const mockClusters = [
  {
    id: "ALL",
    name: "All Clusters",
    farm_ids: [],
  },
  {
    id: "CLUSTER_A",
    name: "Cluster A",
    farm_ids: ["FARM001"],
  },
  {
    id: "CLUSTER_B",
    name: "Cluster B",
    farm_ids: ["MOCK"],
  },
  {
    id: "CLUSTER_C",
    name: "Cluster C",
    farm_ids: [],
  },
];

export default mockClusters;
