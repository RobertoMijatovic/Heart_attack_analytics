<template>
  <v-container>

    <!-- ==================================================
         KPI KARTICE
    =================================================== -->

    <v-row>
      <v-col cols="12" md="3">
        <v-card
          color="red-lighten-2"
          class="pa-4"
        >
          <div class="text-h6">
            Pacijenti
          </div>

          <div class="text-h4">
            {{ kpis.total_patients || 0 }}
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card
          color="blue-lighten-2"
          class="pa-4"
        >
          <div class="text-h6">
            Prosječna dob
          </div>

          <div class="text-h4">
            {{ Number(kpis.average_age || 0).toFixed(1) }}
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card
          color="green-lighten-2"
          class="pa-4"
        >
          <div class="text-h6">
            Prosječni kolesterol
          </div>

          <div class="text-h4">
            {{ Number(kpis.average_cholesterol || 0).toFixed(1) }}
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="3">
        <v-card
          color="purple-lighten-2"
          class="pa-4"
        >
          <div class="text-h6">
            Prosječni BMI
          </div>

          <div class="text-h4">
            {{ Number(kpis.average_bmi || 0).toFixed(1) }}
          </div>
        </v-card>
      </v-col>
    </v-row>

    <!-- ==================================================
         RETRAIN GUMB
    =================================================== -->

    <v-row class="mt-4 mb-2">
      <v-col
        cols="12"
        class="d-flex justify-end"
      >
        <v-btn
          color="red-darken-2"
          size="large"
          prepend-icon="mdi-refresh"
          :loading="retraining"
          :disabled="retraining"
          @click="retrainModels"
        >
          {{ retraining ? "Treniranje u tijeku..." : "Retrain Models" }}
        </v-btn>
      </v-col>
    </v-row>

    <!-- Informacija dok traje treniranje -->

    <v-alert
      v-if="retraining"
      type="info"
      variant="tonal"
      class="mb-4"
      prominent
    >
      Modeli se ponovno treniraju. Proces može trajati nekoliko minuta.
      Nemoj zatvarati aplikaciju.
    </v-alert>

    <!-- ==================================================
         GLAVNA KARTICA I TABOVI
    =================================================== -->

    <v-card class="mt-4">
      <v-tabs
        v-model="tab"
        bg-color="red-lighten-2"
      >
        <v-tab value="eda1">
          EDA – Brojevi
        </v-tab>

        <v-tab value="eda2">
          EDA – Grafovi
        </v-tab>

        <v-tab value="pred">
          Predikcija
        </v-tab>
      </v-tabs>

      <v-window v-model="tab">

        <!-- ==================================================
             EDA – BROJEVI
        =================================================== -->

        <v-window-item value="eda1">
          <v-row class="pa-4">

            <!-- Dataset KPI -->

            <v-col cols="12" md="6">
              <v-card class="pa-4">
                <h3 class="mb-4">
                  Dataset KPI
                </h3>

                <v-list>
                  <v-list-item>
                    <template #title>
                      Broj pacijenata
                    </template>

                    <template #subtitle>
                      {{ kpis.total_patients || 0 }}
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template #title>
                      Prosječna dob
                    </template>

                    <template #subtitle>
                      {{ Number(kpis.average_age || 0).toFixed(1) }}
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template #title>
                      Prosječni kolesterol
                    </template>

                    <template #subtitle>
                      {{ Number(kpis.average_cholesterol || 0).toFixed(1) }}
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template #title>
                      Prosječni krvni tlak
                    </template>

                    <template #subtitle>
                      {{ Number(kpis.average_resting_bp || 0).toFixed(1) }}
                    </template>
                  </v-list-item>

                  <v-list-item>
                    <template #title>
                      Prosječni BMI
                    </template>

                    <template #subtitle>
                      {{ Number(kpis.average_bmi || 0).toFixed(1) }}
                    </template>
                  </v-list-item>
                </v-list>
              </v-card>
            </v-col>

            <!-- Model Performance -->

            <v-col cols="12" md="6">
              <v-card class="pa-4">
                <h3 class="mb-4">
                  Model Performance
                </h3>

                <v-card
                  variant="outlined"
                  class="pa-4"
                >
                  <h3 class="mb-3">
                    Random Forest
                  </h3>

                  <p>
                    Accuracy:
                    {{ formatMetric(metrics.random_forest?.accuracy) }}
                  </p>

                  <p>
                    Precision:
                    {{ formatMetric(metrics.random_forest?.precision) }}
                  </p>

                  <p>
                    Recall:
                    {{ formatMetric(metrics.random_forest?.recall) }}
                  </p>

                  <p>
                    F1-score:
                    {{ formatMetric(metrics.random_forest?.f1) }}
                  </p>

                  <v-divider class="my-4" />

                  <h3 class="mb-3">
                    Deep Learning
                  </h3>

                  <p>
                    Accuracy:
                    {{ formatMetric(metrics.deep_learning?.accuracy) }}
                  </p>

                  <p>
                    Precision:
                    {{ formatMetric(metrics.deep_learning?.precision) }}
                  </p>

                  <p>
                    Recall:
                    {{ formatMetric(metrics.deep_learning?.recall) }}
                  </p>

                  <p>
                    F1-score:
                    {{ formatMetric(metrics.deep_learning?.f1) }}
                  </p>
                </v-card>
              </v-card>
            </v-col>

          </v-row>
        </v-window-item>

        <!-- ==================================================
             EDA – GRAFOVI
        =================================================== -->

        <v-window-item value="eda2">
          <v-container>
            <v-row>

              <!-- Age Distribution -->

              <v-col cols="12" md="4">
                <v-card class="pa-3">
                  <div class="text-h6 mb-3">
                    Age Distribution
                  </div>

                  <img
                    v-if="agePlot"
                    :src="getPlotUrl(agePlot)"
                    alt="Age distribution"
                    class="plot-image"
                    @click="openPlot(agePlot)"
                  />

                  <v-alert
                    v-else
                    type="warning"
                    variant="tonal"
                  >
                    Graf nije pronađen.
                  </v-alert>
                </v-card>
              </v-col>

              <!-- Cholesterol vs Risk -->

              <v-col cols="12" md="4">
                <v-card class="pa-3">
                  <div class="text-h6 mb-3">
                    Cholesterol vs Risk
                  </div>

                  <img
                    v-if="cholesterolPlot"
                    :src="getPlotUrl(cholesterolPlot)"
                    alt="Cholesterol versus risk"
                    class="plot-image"
                    @click="openPlot(cholesterolPlot)"
                  />

                  <v-alert
                    v-else
                    type="warning"
                    variant="tonal"
                  >
                    Graf nije pronađen.
                  </v-alert>
                </v-card>
              </v-col>

              <!-- Correlation Heatmap -->

              <v-col cols="12" md="4">
                <v-card class="pa-3">
                  <div class="text-h6 mb-3">
                    Correlation Heatmap
                  </div>

                  <img
                    v-if="corrPlot"
                    :src="getPlotUrl(corrPlot)"
                    alt="Correlation heatmap"
                    class="plot-image"
                    @click="openPlot(corrPlot)"
                  />

                  <v-alert
                    v-else
                    type="warning"
                    variant="tonal"
                  >
                    Graf nije pronađen.
                  </v-alert>
                </v-card>
              </v-col>

            </v-row>

            <!-- Uvećani prikaz grafa -->

            <v-dialog
              v-model="dialog"
              max-width="90%"
            >
              <v-card>
                <v-card-title class="d-flex justify-space-between align-center">
                  <span>Uvećani prikaz grafa</span>

                  <v-btn
                    icon="mdi-close"
                    variant="text"
                    @click="dialog = false"
                  />
                </v-card-title>

                <v-divider />

                <v-card-text>
                  <v-img
                    :src="selectedImage"
                    max-height="80vh"
                    contain
                  />
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-container>
        </v-window-item>

        <!-- ==================================================
             PREDIKCIJA
        =================================================== -->

        <v-window-item value="pred">
          <v-card class="pa-4 mb-4">
            <v-row>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.age"
                  type="number"
                  label="Age"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="form.gender"
                  :items="['male', 'female']"
                  label="Gender"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.resting_bp"
                  type="number"
                  label="Resting BP"
                  :error="Number(form.resting_bp) > highRisk.resting_bp"
                  :hint="
                    Number(form.resting_bp) > highRisk.resting_bp
                      ? 'High BP ⚠️'
                      : ''
                  "
                  persistent-hint
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.cholesterol"
                  type="number"
                  label="Cholesterol"
                  :error="Number(form.cholesterol) > highRisk.cholesterol"
                  :hint="
                    Number(form.cholesterol) > highRisk.cholesterol
                      ? 'High cholesterol ⚠️'
                      : ''
                  "
                  persistent-hint
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.max_heart_rate"
                  type="number"
                  label="Max Heart Rate"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.bmi"
                  type="number"
                  label="BMI"
                  :error="Number(form.bmi) > highRisk.bmi"
                  :hint="
                    Number(form.bmi) > highRisk.bmi
                      ? 'High BMI ⚠️'
                      : ''
                  "
                  persistent-hint
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-text-field
                  v-model="form.stress_level"
                  type="number"
                  label="Stress Level"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-select
                  v-model="form.smoking_status"
                  :items="['never', 'former', 'current']"
                  label="Smoking Status"
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-switch
                  v-model="form.diabetes"
                  color="red"
                  :label="
                    form.diabetes
                      ? 'Diabetes: YES'
                      : 'Diabetes: NO'
                  "
                />
              </v-col>

              <v-col cols="12" md="6">
                <v-switch
                  v-model="form.family_history"
                  color="red"
                  :label="
                    form.family_history
                      ? 'Family history: YES'
                      : 'Family history: NO'
                  "
                />
              </v-col>

            </v-row>

            <v-btn
              color="red"
              class="mt-2"
              :loading="predicting"
              :disabled="predicting || retraining"
              @click="predictRisk"
            >
              Predict
            </v-btn>
          </v-card>

          <!-- Rezultat predikcije -->

          <v-card
            v-if="result"
            class="mt-6 pa-4"
            :color="
              result.risk.includes('High')
                ? 'red-lighten-2'
                : result.risk.includes('Medium')
                  ? 'orange-lighten-2'
                  : 'green-lighten-2'
            "
          >
            <div class="text-h6">
              Prediction Result
            </div>

            <div class="text-h5 mt-2">
              {{ result.risk }}
            </div>

            <div class="mt-2">
              Final score:
              {{ Number(result.final_score).toFixed(2) }}
            </div>

            <div>
              RF:
              {{ Number(result.rf_pred).toFixed(2) }}
              |
              DL:
              {{ Number(result.dl_pred).toFixed(2) }}
            </div>
          </v-card>

          <!-- Objašnjenje ulaznih faktora -->

          <v-card
            v-if="explanation.length"
            class="mt-4 pa-4"
          >
            <div class="text-h6">
              Why is this a risk?
            </div>

            <v-chip
              v-for="(reason, index) in explanation"
              :key="index"
              class="ma-1"
              color="red"
              variant="flat"
            >
              {{ reason }}
            </v-chip>
          </v-card>

          <!-- Doughnut graf -->

          <div
            v-show="result"
            class="mt-6 chart-container"
          >
            <canvas ref="chartRef"></canvas>
          </div>
        </v-window-item>

      </v-window>
    </v-card>

    <!-- ==================================================
         PORUKE
    =================================================== -->

    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      timeout="5000"
    >
      {{ snackbarMessage }}

      <template #actions>
        <v-btn
          variant="text"
          @click="snackbar = false"
        >
          Zatvori
        </v-btn>
      </template>
    </v-snackbar>

  </v-container>
</template>

<script setup>
import {
  ref,
  onMounted,
  nextTick,
  computed
} from "vue"

import api from "../api/api"

import {
  Chart,
  ArcElement,
  Tooltip,
  Legend,
  DoughnutController
} from "chart.js"


Chart.register(
  ArcElement,
  Tooltip,
  Legend,
  DoughnutController
)


/* ==================================================
   OSNOVNE POSTAVKE
=================================================== */

const API_BASE =
  api.defaults.baseURL || "http://127.0.0.1:8000"

const tab = ref("eda1")

const kpis = ref({})
const metrics = ref({})

const plots = ref([])
const agePlot = ref("")
const cholesterolPlot = ref("")
const corrPlot = ref("")

const plotVersion = ref(Date.now())

const dialog = ref(false)
const selectedImage = ref("")

const retraining = ref(false)
const predicting = ref(false)

const snackbar = ref(false)
const snackbarMessage = ref("")
const snackbarColor = ref("success")


/* ==================================================
   PREDIKCIJSKA FORMA
=================================================== */

const form = ref({
  age: 50,
  gender: "male",
  resting_bp: 120,
  cholesterol: 200,
  max_heart_rate: 150,
  bmi: 25,
  stress_level: 5,
  smoking_status: "never",
  diabetes: false,
  family_history: false
})

const result = ref(null)


/* ==================================================
   PRAGOVI RIZIKA
=================================================== */

const highRisk = {
  cholesterol: 240,
  resting_bp: 140,
  bmi: 30
}


/* ==================================================
   OBJAŠNJENJE RIZIKA
=================================================== */

const explanation = computed(() => {
  const reasons = []

  if (Number(form.value.cholesterol) > 240) {
    reasons.push("High cholesterol")
  }

  if (Number(form.value.bmi) > 30) {
    reasons.push("High BMI")
  }

  if (Number(form.value.resting_bp) > 140) {
    reasons.push("High blood pressure")
  }

  if (form.value.diabetes) {
    reasons.push("Diabetes present")
  }

  if (form.value.family_history) {
    reasons.push("Family history")
  }

  return reasons
})


/* ==================================================
   POMOĆNE FUNKCIJE
=================================================== */

function formatMetric(value) {
  if (value === undefined || value === null) {
    return "N/A"
  }

  return Number(value).toFixed(3)
}


function showMessage(message, color = "success") {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}


function getPlotUrl(filename) {
  if (!filename) {
    return ""
  }

  return (
    `${API_BASE}/artifacts/${filename}` +
    `?version=${plotVersion.value}`
  )
}


function openPlot(filename) {
  selectedImage.value = getPlotUrl(filename)
  dialog.value = true
}


/* ==================================================
   CHART.JS
=================================================== */

const chartRef = ref(null)

let chartInstance = null


function renderChart(score) {
  if (!chartRef.value) {
    return
  }

  const ctx = chartRef.value.getContext("2d")

  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(ctx, {
    type: "doughnut",

    data: {
      labels: [
        "Risk",
        "Safe"
      ],

      datasets: [
        {
          data: [
            score,
            1 - score
          ],

          backgroundColor: [
            "#e53935",
            "#43a047"
          ]
        }
      ]
    },

    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}


/* ==================================================
   DOHVAT KPI-JEVA I METRIKA
=================================================== */

async function loadKpis() {
  try {
    const [
      kpiResponse,
      metricResponse
    ] = await Promise.all([
      api.get("/kpis"),
      api.get("/metrics")
    ])

    kpis.value = kpiResponse.data
    metrics.value = metricResponse.data

  } catch (error) {
    console.error(
      "Greška pri učitavanju KPI-jeva:",
      error
    )

    showMessage(
      "KPI pokazatelji i metrike nisu učitani.",
      "error"
    )
  }
}


/* ==================================================
   DOHVAT EDA GRAFOVA
=================================================== */

async function loadPlots() {
  try {
    const response = await api.get("/plots")

    plots.value = response.data.plots || []

    agePlot.value =
      plots.value.find(
        plot => plot.includes("age")
      ) || ""

    cholesterolPlot.value =
      plots.value.find(
        plot => plot.includes("cholesterol")
      ) || ""

    corrPlot.value =
      plots.value.find(
        plot => plot.includes("correlation")
      ) || ""

  } catch (error) {
    console.error(
      "Greška pri učitavanju grafova:",
      error
    )

    showMessage(
      "EDA grafovi nisu učitani.",
      "error"
    )
  }
}


/* ==================================================
   PREDIKCIJA
=================================================== */

async function predictRisk() {
  try {
    predicting.value = true

    const requestData = {
      age: Number(form.value.age),
      gender: form.value.gender,
      resting_bp: Number(form.value.resting_bp),
      cholesterol: Number(form.value.cholesterol),
      max_heart_rate: Number(form.value.max_heart_rate),
      bmi: Number(form.value.bmi),
      stress_level: Number(form.value.stress_level),
      smoking_status: form.value.smoking_status,
      diabetes: form.value.diabetes ? 1 : 0,
      family_history: form.value.family_history ? 1 : 0
    }

    const response = await api.post(
      "/predict",
      requestData
    )

    result.value = response.data

    await nextTick()

    renderChart(
      Number(response.data.final_score)
    )

  } catch (error) {
    console.error(
      "Greška tijekom predikcije:",
      error
    )

    const message =
      error.response?.data?.detail ||
      "Predikcija nije uspjela."

    showMessage(
      message,
      "error"
    )

  } finally {
    predicting.value = false
  }
}


/* ==================================================
   PONOVNO TRENIRANJE MODELA
=================================================== */

async function retrainModels() {
  const confirmed = window.confirm(
    "Želiš li ponovno istrenirati modele? " +
    "Proces može trajati nekoliko minuta."
  )

  if (!confirmed) {
    return
  }

  try {
    retraining.value = true

    await api.post("/retrain")

    /*
     * Backend je završio:
     * - treniranje modela
     * - generiranje KPI-jeva
     * - generiranje metrika
     * - generiranje novih PNG grafova
     */

    await Promise.all([
      loadKpis(),
      loadPlots()
    ])

    /*
     * Mijenjanjem verzije URL-a prisiljavamo preglednik
     * da ponovno preuzme slike umjesto korištenja cachea.
     */
    plotVersion.value = Date.now()

    result.value = null

    if (chartInstance) {
      chartInstance.destroy()
      chartInstance = null
    }

    showMessage(
      "Modeli, KPI pokazatelji, metrike i grafovi uspješno su ažurirani.",
      "success"
    )

  } catch (error) {
    console.error(
      "Greška tijekom ponovnog treniranja:",
      error
    )

    const message =
      error.response?.data?.detail ||
      "Ponovno treniranje modela nije uspjelo."

    showMessage(
      message,
      "error"
    )

  } finally {
    retraining.value = false
  }
}


/* ==================================================
   POKRETANJE KOMPONENTE
=================================================== */

onMounted(async () => {
  await Promise.all([
    loadKpis(),
    loadPlots()
  ])
})
</script>

<style scoped>
.plot-image {
  width: 100%;
  display: block;
  cursor: pointer;
  transition:
    transform 0.2s ease,
    opacity 0.2s ease;
}

.plot-image:hover {
  transform: scale(1.02);
  opacity: 0.9;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 320px;
}
</style>