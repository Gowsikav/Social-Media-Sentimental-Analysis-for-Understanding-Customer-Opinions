document.addEventListener("DOMContentLoaded", function () {
  const analyzeBtn = document.getElementById("analyze-btn");
  const loadingSection = document.getElementById("loading-section");
  const resultsSection = document.getElementById("results-section");
  const sentimentChart = document.getElementById("sentimentChart");
  const suggestion = document.getElementById("suggestion");

  analyzeBtn.addEventListener("click", function () {
    const productUrl = document.getElementById("productUrl").value;

    loadingSection.style.display = "block";
    resultsSection.style.display = "none";

    fetch("/analyze-sentiment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        productUrl: productUrl,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data.error) {
          suggestion.textContent = data.error;
          loadingSection.style.display = "none";
          resultsSection.style.display = "block";
          return;
        }

        const positiveCount = data.positive || 0;
        const negativeCount = data.negative || 0;
        const neutralCount = data.neutral || 0;

        sentimentChart.innerHTML = "";
        new Chart(sentimentChart, {
          type: "pie",
          data: {
            labels: ["Positive", "Negative", "Neutral"],
            datasets: [
              {
                label: "Sentiment Analysis",
                backgroundColor: ["green", "red", "blue"],
                data: [positiveCount, negativeCount, neutralCount],
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            aspectRatio: 1,
            cutoutPercentage: 50,
            plugins: {
              legend: {
                position: "bottom",
              },
            },
          },
        });

        const overallSentiment = getOverallSentiment(data);
        suggestion.textContent = generateSuggestion(overallSentiment);

        loadingSection.style.display = "none";
        resultsSection.style.display = "block";
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

  function getOverallSentiment(sentimentData) {
    const totalReviews =
      (sentimentData.positive || 0) +
      (sentimentData.negative || 0) +
      (sentimentData.neutral || 0);
    const positivePercentage =
      ((sentimentData.positive || 0) / totalReviews) * 100;
    const negativePercentage =
      ((sentimentData.negative || 0) / totalReviews) * 100;

    if (positivePercentage >= 60) {
      return "positive";
    } else if (negativePercentage >= 40) {
      return "negative";
    } else {
      return "neutral";
    }
  }

  function generateSuggestion(sentiment) {
    const suggestions = {
      positive:
        "Based on the positive sentiment of the reviews, this product seems to be well-received by customers. You can confidently consider purchasing it.",
      negative:
        "The negative sentiment in the reviews indicates some issues with this product. It's advisable to read the negative reviews carefully before making a decision.",
      neutral:
        "The reviews for this product have mixed sentiments, indicating varying experiences. It's recommended to explore further and consider individual factors before deciding.",
    };
    return suggestions[sentiment];
  }
});
