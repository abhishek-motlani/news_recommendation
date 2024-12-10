import React, { useState } from "react";
import axios from "axios";
import "./styles.css";

const SearchBar = () => {
  const [query, setQuery] = useState("");
  const [username, setUsername] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [personalRecommendations, setPersonalRecommendations] = useState([]);
  const [activeTab, setActiveTab] = useState("search"); // To manage active tab
  const [error, setError] = useState("");

  const handleSearch = async () => {
    try {
      // Clear other states and fetch search recommendations
      setPersonalRecommendations([]);
      setError("");
      const response = await axios.post("http://127.0.0.1:8000/recommend", {
        text: query,
      });
      setRecommendations(response.data.recommendations);
    } catch (err) {
      setError("Error fetching recommendations. Please try again.");
      console.error(err);
    }
  };

  const handlePersonalRecommendations = async () => {
    try {
      // Clear other states and fetch personalized recommendations
      setRecommendations([]);
      setError("");
      const response = await axios.post(
        "http://127.0.0.1:8000/personal_recommend",
        { text: username }
      );
      setPersonalRecommendations(response.data.recommendations);
    } catch (err) {
      setError(
        "Error fetching personalized recommendations or no recommendations available. Please try again."
      );
      console.error(err);
    }
  };

  const handleLikeDislike = async (id, action, type) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/log_interaction",
        {
          username,
          article_id: id.toString(),
          action, // 'like', 'dislike', or 'read_more_click'
          action_type: type,
        }
      );
      console.log("Interaction logged:", response.data);
    } catch (err) {
      console.error("Error logging interaction:", err);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>News Recommendation</h1>
        <p>Find the news tailored to your interests.</p>
      </div>

      {/* Input Fields */}
      <div className="search-container">
        <input
          type="text"
          className="input username-input"
          placeholder="Enter your username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="text"
          className="input search-input"
          placeholder="Search news..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button className="search-button" onClick={handleSearch}>
          Search
        </button>
        <button
          className="search-button"
          onClick={handlePersonalRecommendations}
          disabled={!username}
        >
          Get Personalized Recommendations
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {/* Tabs */}
      <div className="tabs">
        <button
          className={`tab ${activeTab === "search" ? "active-tab" : ""}`}
          onClick={() => setActiveTab("search")}
        >
          Search Recommendations
        </button>
        <button
          className={`tab ${activeTab === "personal" ? "active-tab" : ""}`}
          onClick={() => setActiveTab("personal")}
        >
          Personalized Recommendations
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === "search" && (
          <div className="recommendations">
            {recommendations.length > 0 ? (
              recommendations.map((rec, index) => (
                <div key={index} className="news-item">
                  <h3>{rec.title}</h3>
                  <p>{rec.description}</p>
                  <a
                    href={rec.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="read-more"
                    onClick={() =>
                      handleLikeDislike(rec.id, "read_more", "searched")
                    }
                  >
                    Read more
                  </a>
                  <div className="actions">
                    <button
                      className="like-button"
                      onClick={() =>
                        handleLikeDislike(rec.id, "like", "searched")
                      }
                    >
                      👍 Like
                    </button>
                    <button
                      className="dislike-button"
                      onClick={() =>
                        handleLikeDislike(rec.id, "dislike", "searched")
                      }
                    >
                      👎 Dislike
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <p>No search recommendations available. Try searching!</p>
            )}
          </div>
        )}
        {activeTab === "personal" && (
          <div className="recommendations">
            {personalRecommendations.length > 0 ? (
              personalRecommendations.map((rec, index) => (
                <div key={index} className="news-item">
                  <h3>{rec.title}</h3>
                  <p>{rec.description}</p>
                  <a
                    href={rec.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="read-more"
                    onClick={() =>
                      handleLikeDislike(rec.id, "read_more", "recommended")
                    }
                  >
                    Read more
                  </a>
                  <div className="actions">
                    <button
                      className="like-button"
                      onClick={() =>
                        handleLikeDislike(rec.id, "like", "recommended")
                      }
                    >
                      👍 Like
                    </button>
                    <button
                      className="dislike-button"
                      onClick={() =>
                        handleLikeDislike(rec.id, "dislike", "recommended")
                      }
                    >
                      👎 Dislike
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <p>No personalized recommendations available.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchBar;
