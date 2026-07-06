<template>
  <v-app>
    <v-app-bar color="red-darken-2">
      <v-toolbar-title>
         Heart Attack Analytics Dashboard
      </v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid class="pa-6">
        <Dashboard />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import Dashboard from "./components/Dashboard.vue"
</script>