<template>
    <div class="container">
        <div class="row col-12">
            <h1 class="text-center">Searching Places of Interest</h1>
            <form class="row row-cols-lg align-items-center justify-content-center" action="#"
                style="margin-bottom: 20px;">
                <div class="row col-10">
                    <label for="colFormLabelLg" class="col-sm-2 col-form-label col-form-label-lg">Place Name</label>
                    <div class="col-sm-10">
                        <input type="text" class="form-control form-control-lg" id="colFormLabelLg"
                            @keyup.enter="searchPlaces" v-model="query" placeholder="Place Name">
                    </div>
                </div>
                <div class="col-2">
                    <button type="button" class="btn btn-success" @click="searchPlaces">Search This Place</button>
                </div>
            </form>


        </div>
        <div id="map" style="width: 100%; min-height:600px; height: 100%;"></div>
    </div>
</template>

<script>
import mapboxgl from "mapbox-gl";
import axios from "axios";

export default {
    data() {
        return {
            map: null,
            markers: [],
            query: "",
            mapboxToken: "pk.eyJ1IjoieXVwZW5nbGl1IiwiYSI6ImNtMjF2a2lpNDAwa28ybXEwNzByeHZkdjEifQ.eJuvRXNJcqKUbAFBwu5xJg", // Mapbox Access Token
        };
    },
    mounted() {
        // 初始化 Mapbox 地图
        this.initializeMap();
    },
    methods: {
        initializeMap() {
            mapboxgl.accessToken = this.mapboxToken;

            this.map = new mapboxgl.Map({
                container: "map", // map container id
                style: "mapbox://styles/mapbox/streets-v11", // map style
                center: [144.9634, -37.8130], // map center
                zoom: 10, // initial zoom level
            });

            // add navigation controls to 
            this.map.addControl(new mapboxgl.NavigationControl());
        },

        async searchPlaces() {
            if (!this.query) return;

            // use Mapbox Geocoding API to search
            const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${this.query}.json?access_token=${this.mapboxToken}&limit=10`;

            try {
                const response = await axios.get(url);
                const results = response.data.features;

                // clear old markers
                this.clearMarkers();

                // foreach result, create a marker and add it to the map
                results.forEach((place) => {
                    const [lng, lat] = place.geometry.coordinates;

                    // create a marker
                    const marker = new mapboxgl.Marker()
                        .setLngLat([lng, lat])
                        .addTo(this.map);

                    // save the marker
                    this.markers.push(marker);
                });

                // make the map center to the first result
                if (results.length > 0) {
                    const [lng, lat] = results[0].geometry.coordinates;
                    this.map.flyTo({ center: [lng, lat], zoom: 14 });
                }
            } catch (error) {
                console.error("Error fetching places:", error);
            }
        },

        clearMarkers() {
            // clear all markers
            this.markers.forEach((marker) => marker.remove());
            this.markers = [];
        },
    },
};
</script>

<style>
/* Optional: 添加样式 */
#map {
    border: 2px solid #ccc;
    border-radius: 10px;
}
</style>