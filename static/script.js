document.addEventListener("DOMContentLoaded", function () {
    
    mapboxgl.accessToken = MAPBOX_ACCESS_TOKEN;
    const map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v11",
        center: [145.12, -37.92], 
        zoom: 10
    });

    let marker = new mapboxgl.Marker().setLngLat([145.12, -37.92]).addTo(map);
    let cancerChart = null;

    function fetchUV(lat, lng) {
        fetch(`/api/uv?lat=${lat}&lng=${lng}`)
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    document.getElementById("uvIndex").innerText = data.result.uv;
                    document.getElementById("uvMax").innerText = data.result.uv_max;
                } else {
                    console.error("UV fail:", data);
                }
            })
            .catch(error => console.error("❌ UV API fail:", error));
    }

    window.searchLocation = function () {
        const location = document.getElementById("locationInput").value;
        if (!location) return alert("Type the city name");

        fetch(`/api/mapbox?location=${location}`)
            .then(response => response.json())
            .then(data => {
                if (data.features && data.features.length > 0) {
                    let [lng, lat] = data.features[0].center;
                    map.flyTo({ center: [lng, lat], zoom: 12 });
                    marker.setLngLat([lng, lat]);
                    fetchUV(lat, lng);
                } else {
                    alert("Cannot find the city");
                }
            })
            .catch(error => console.error("❌ Can not get geo code:", error));
    };

    window.getCurrentLocation = function() {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                let lat = position.coords.latitude;
                let lng = position.coords.longitude;
                map.flyTo({ center: [lng, lat], zoom: 8 });
                marker.setLngLat([lng, lat]);
                fetchUV(lat, lng);
            },
            (error) => {
                alert("Fail to get location");
            }
        );
    };

    window.fetchCancerData = function () {
        const state = document.getElementById("stateSelect").value;
        const cancerType = document.querySelector('input[name="cancerType"]:checked');

        if (!state || !cancerType) {
            alert("Please select a state and a data type.");
            return;
        }

        fetch(`/api/cancer_data?state=${state}&type=${cancerType.value}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) {
                    alert("No data found.");
                    return;
                }
                let years = data.map(item => item[0]);
                let counts = data.map(item => item[1]);

                if (cancerChart) {
                    cancerChart.destroy();
                }

                const ctx = document.getElementById("cancerChart").getContext("2d");
                cancerChart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: years,
                        datasets: [{
                            label: `${cancerType.value} Cases`,
                            data: counts,
                            backgroundColor: "rgba(75, 192, 192, 0.6)",
                            borderColor: "rgba(75, 192, 192, 1)",
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: { y: { beginAtZero: true } }
                    }
                });
            })
            .catch(error => console.error("❌ Error fetching cancer data:", error));
    };

    fetchUV(-37.92, 145.12);
});
