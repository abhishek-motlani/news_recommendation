import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Container,
  Typography,
  Paper,
  Box,
  Button,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import {
  VictoryBar,
  VictoryChart,
  VictoryAxis,
  VictoryTheme,
  VictoryTooltip,
  VictoryPie,
  VictoryLine,
} from "victory";

const Dashboard = () => {
  const [popularArticles, setPopularArticles] = useState([]);
  const [userStats, setUserStats] = useState([]);
  const [recentArticles, setRecentArticles] = useState([]);
  const [categoryInteractions, setCategoryInteractions] = useState([]);
  const [expandedDashboard, setExpandedDashboard] = useState(null);
  const [actionBreakdown, setActionBreakdown] = useState([]);

  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  useEffect(() => {
    axios
      .get("http://localhost:8000/popular-articles/")
      .then((res) => setPopularArticles(res.data))
      .catch((err) => console.error(err));

    axios
      .get("http://localhost:8000/user-stats/")
      .then((res) => setUserStats(res.data))
      .catch((err) => console.error(err));

    axios
      .get("http://localhost:8000/recent-articles/")
      .then((res) => setRecentArticles(res.data))
      .catch((err) => console.error(err));

    axios
      .get("http://localhost:8000/category-interactions/")
      .then((res) => setCategoryInteractions(res.data))
      .catch((err) => console.error(err));

    axios
      .get("http://localhost:8000/action-breakdown/")
      .then((res) => setActionBreakdown(res.data))
      .catch((err) => console.error(err));
  }, []);

  const renderPlaceholderChart = (type) => {
    switch (type) {
      case "bar":
        return (
          <VictoryChart
            theme={VictoryTheme.material}
            domainPadding={10}
            width={200}
            height={150}
          >
            <VictoryBar
              data={[
                { x: "A", y: 10 },
                { x: "B", y: 15 },
                { x: "C", y: 20 },
              ]}
              style={{ data: { fill: "#4caf50" } }}
            />
          </VictoryChart>
        );
      case "pie":
        return (
          <VictoryPie
            data={[
              { x: "A", y: 30 },
              { x: "B", y: 40 },
              { x: "C", y: 30 },
            ]}
            colorScale={["#ff5722", "#4caf50", "#2196f3"]}
            width={200}
            height={150}
          />
        );
      case "line":
        return (
          <VictoryChart
            theme={VictoryTheme.material}
            domainPadding={10}
            width={200}
            height={150}
          >
            <VictoryLine
              data={[
                { x: 1, y: 10 },
                { x: 2, y: 15 },
                { x: 3, y: 12 },
                { x: 4, y: 20 },
              ]}
              style={{
                data: { stroke: "#ff9800", strokeWidth: 3 },
              }}
            />
          </VictoryChart>
        );
      default:
        return null;
    }
  };

  const renderDashboard = (key, isSmallScreen) => {
    const width = isSmallScreen ? 350 : 700;
    const height = isSmallScreen ? 250 : 400;

    switch (key) {
      case "popularArticles":
        return (
          <Paper style={{ margin: "20px 0", padding: "20px" }}>
            <Typography variant="h6" gutterBottom align="center">
              Most Liked Articles
            </Typography>
            <VictoryChart
              theme={VictoryTheme.material}
              domainPadding={20}
              width={width}
              height={height}
            >
              <VictoryAxis
                tickFormat={(t) => (t.length > 15 ? `${t.slice(0, 15)}...` : t)}
                label="Article Titles"
                style={{
                  axisLabel: { fontSize: 12, padding: 30 },
                  tickLabels: { fontSize: 8, angle: isSmallScreen ? -45 : 0 },
                }}
              />
              <VictoryAxis
                dependentAxis
                label="Likes"
                style={{
                  axisLabel: { fontSize: 12, padding: 40 },
                  tickLabels: { fontSize: 8 },
                }}
              />
              <VictoryBar
                data={
                  popularArticles.length > 0
                    ? popularArticles
                    : [{ title: "No Data", likes: 0 }]
                }
                x="title"
                y="likes"
                style={{ data: { fill: "#4caf50" } }}
              />
            </VictoryChart>
          </Paper>
        );

      case "userStats":
        return (
          <Paper style={{ margin: "20px 0", padding: "20px" }}>
            <Typography variant="h6" gutterBottom align="center">
              User Activity
            </Typography>
            {userStats.length > 0 ? (
              <VictoryChart
                theme={VictoryTheme.material}
                domainPadding={20}
                width={width}
                height={height}
              >
                <VictoryAxis
                  tickFormat={(t) =>
                    t.length > 10 ? `${t.slice(0, 10)}...` : t
                  }
                  label="User IDs"
                  style={{
                    axisLabel: { fontSize: 12, padding: 30 },
                    tickLabels: { fontSize: 8, angle: isSmallScreen ? -45 : 0 },
                  }}
                />
                <VictoryAxis
                  dependentAxis
                  label="Total Actions"
                  style={{
                    axisLabel: { fontSize: 12, padding: 40 },
                    tickLabels: { fontSize: 8 },
                  }}
                />
                <VictoryBar
                  data={userStats}
                  x="_id"
                  y="total_actions"
                  style={{ data: { fill: "#2196f3" } }}
                />
              </VictoryChart>
            ) : (
              <Typography variant="body1" align="center">
                No user activity data available
              </Typography>
            )}
          </Paper>
        );

      case "recentArticles":
        return (
          <Paper style={{ margin: "10px 0", padding: "20px" }}>
            <Typography variant="h4" gutterBottom align="center">
              Recent Articles Engagement
            </Typography>
            <VictoryChart
              theme={VictoryTheme.material}
              width={width}
              height={height}
            >
              <VictoryAxis
                label="Published Date"
                style={{
                  axisLabel: { fontSize: 12, padding: 35 },
                  tickLabels: {
                    fontSize: 10,
                    padding: 15,
                    angle: isSmallScreen ? -60 : 0,
                  },
                }}
                tickFormat={(x) =>
                  new Date(x).toLocaleDateString("en-US", {
                    month: "short",
                    day: "numeric",
                  })
                }
                tickCount={isSmallScreen ? 5 : 10}
              />
              <VictoryAxis
                dependentAxis
                label="Interactions"
                style={{
                  axisLabel: { fontSize: 12, padding: 40 },
                  tickLabels: { fontSize: 10 },
                }}
              />
              <VictoryLine
                data={recentArticles}
                x="published_at"
                y="interactions"
                style={{
                  data: {
                    stroke: "#ff9800",
                    strokeWidth: 3,
                  },
                  parent: {
                    border: "1px solid #ccc",
                  },
                }}
              />
            </VictoryChart>
          </Paper>
        );

      case "categoryInteractions":
        return (
          <Paper style={{ margin: "20px 0", padding: "20px" }}>
            <Typography variant="h4" gutterBottom align="center">
              Article Popularity by Category
            </Typography>
            <VictoryPie
              data={categoryInteractions}
              x="category"
              y="interactions"
              labels={({ datum }) =>
                `${datum.category}: ${datum.interactions} (${(
                  (datum.interactions /
                    categoryInteractions.reduce(
                      (acc, curr) => acc + curr.interactions,
                      0
                    )) *
                  100
                ).toFixed(1)}%)`
              }
              colorScale="qualitative"
              style={{
                labels: {
                  fontSize: 12,
                  fill: "white",
                  padding: 5,
                },
                data: { stroke: "#fff", strokeWidth: 2 },
              }}
              labelComponent={
                <VictoryTooltip
                  flyoutStyle={{ fill: "green" }}
                  style={{ fontSize: 10, fill: "white" }}
                />
              }
              width={width}
              height={height}
            />
          </Paper>
        );

      case "actionBreakdown":
        return (
          <Paper style={{ margin: "20px 0", padding: "20px" }}>
            <Typography variant="h6" gutterBottom align="center">
              Top Actions by Users
            </Typography>
            <VictoryChart
              theme={VictoryTheme.material}
              domainPadding={{ x: [30, 30] }}
              width={width}
              height={height}
            >
              <VictoryAxis
                label="Action Types"
                style={{
                  axisLabel: { fontSize: 12, padding: 25 },
                  tickLabels: {
                    fontSize: 10,
                    padding: 5,
                    angle: isSmallScreen ? -45 : 0,
                  },
                }}
              />
              <VictoryAxis
                dependentAxis
                label="Counts"
                style={{
                  axisLabel: { fontSize: 12, padding: 30 },
                  tickLabels: { fontSize: 10 },
                }}
              />
              <VictoryBar
                data={actionBreakdown}
                x="action"
                y="count"
                style={{
                  data: { fill: "#3f51b5", stroke: "#fff", strokeWidth: 2 },
                  labels: { fontSize: 10, fill: "#333", fontWeight: "bold" },
                }}
                labelComponent={
                  <VictoryTooltip
                    flyoutStyle={{ fill: "black" }}
                    style={{ fontSize: 10, fill: "white" }}
                  />
                }
                animate={{
                  duration: 500,
                  onExit: { duration: 500 },
                }}
              />
            </VictoryChart>
          </Paper>
        );

      default:
        return null;
    }
  };
  const DashboardCompactView = ({ title, placeholderType, onExpand }) => (
    <Paper
      style={{
        margin: "10px",
        padding: "20px",
        cursor: "pointer",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        width: "250px",
        height: "300px",
        justifyContent: "space-between",
      }}
    >
      <Typography variant="h6" align="center" gutterBottom>
        {title}
      </Typography>
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        flex="1"
        width="100%"
        marginBottom="10px" // Add some margin between chart and button
      >
        {renderPlaceholderChart(placeholderType)}
      </Box>
      <Button
        variant="outlined"
        fullWidth
        onClick={onExpand}
        style={{
          marginTop: "-20px", // Pull the button up
          position: "relative", // Ensure proper positioning
          zIndex: 1, // Ensure button is above chart
        }}
      >
        Expand
      </Button>
    </Paper>
  );

  return (
    <Container maxWidth="lg" style={{ marginTop: "20px" }}>
      <Typography variant="h4" align="center" gutterBottom>
        News Recommendation Dashboard
      </Typography>
      {expandedDashboard ? (
        <Box>
          <Button
            variant="outlined"
            onClick={() => setExpandedDashboard(null)}
            style={{
              marginBottom: "10px",
              position: "sticky",
              top: "10px",
              zIndex: 10,
              backgroundColor: "white",
            }}
          >
            Back to Overview
          </Button>
          {renderDashboard(expandedDashboard, isSmallScreen)}
        </Box>
      ) : (
        <Box
          display="flex"
          justifyContent="center" // Changed from space-between to center
          alignItems="stretch" // Ensure consistent height
          flexWrap="wrap"
          gap="20px" // Add consistent spacing between cards
        >
          <DashboardCompactView
            title="Most Liked Articles"
            placeholderType="bar"
            onExpand={() => setExpandedDashboard("popularArticles")}
          />
          <DashboardCompactView
            title="User Stats"
            placeholderType="bar"
            onExpand={() => setExpandedDashboard("userStats")}
          />
          <DashboardCompactView
            title="Recent Articles"
            placeholderType="line"
            onExpand={() => setExpandedDashboard("recentArticles")}
          />
          <DashboardCompactView
            title="Category Interactions"
            placeholderType="pie"
            onExpand={() => setExpandedDashboard("categoryInteractions")}
          />
          <DashboardCompactView
            title="Top Actions"
            placeholderType="bar"
            onExpand={() => setExpandedDashboard("actionBreakdown")}
          />
        </Box>
      )}
    </Container>
  );
};
export default Dashboard;
