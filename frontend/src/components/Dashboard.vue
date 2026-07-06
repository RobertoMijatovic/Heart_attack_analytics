<template>

<v-container>

    

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
                    {{ kpis.total_patients }}
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



    

    <v-card class="mt-6">

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

            

            <v-window-item value="eda1">

                <v-row class="pa-4">

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
                                        {{ kpis.total_patients }}
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



                    <v-col cols="12" md="6">

                        <v-card class="pa-4">

                            <h3 class="mb-4">
                                Model Performance
                            </h3>

                            <v-list>

                                <v-list-item>

                                    <template #title>
                                        Random Forest
                                    </template>

                                    <template #subtitle>

                                        Accuracy:
                                        {{ metrics.random_forest?.accuracy?.toFixed(3) }}

                                        <br>

                                        Precision:
                                        {{ metrics.random_forest?.precision?.toFixed(3) }}

                                        <br>

                                        Recall:
                                        {{ metrics.random_forest?.recall?.toFixed(3) }}

                                    </template>

                                </v-list-item>

                                <v-divider />

                                <v-list-item>

                                    <template #title>
                                        Deep Learning
                                    </template>

                                    <template #subtitle>

                                        Accuracy:
                                        {{ metrics.deep_learning?.accuracy?.toFixed(3) }}

                                        <br>

                                        Precision:
                                        {{ metrics.deep_learning?.precision?.toFixed(3) }}

                                        <br>

                                        Recall:
                                        {{ metrics.deep_learning?.recall?.toFixed(3) }}

                                    </template>

                                </v-list-item>

                            </v-list>

                        </v-card>

                    </v-col>

                </v-row>

            </v-window-item>



            

            <v-window-item value="eda2">

  <v-container>

    <v-row>

      <v-col cols="12" md="4">

        <v-card class="pa-3">

          <div class="text-h6 mb-3">
            Age Distribution
          </div>

          <img
            :src="`http://127.0.0.1:8000/artifacts/${agePlot}`"
            style="width:100%; cursor:pointer"
            @click="
              selectedImage=`http://127.0.0.1:8000/artifacts/${agePlot}`;
              dialog=true
            "
          >

        </v-card>

      </v-col>

      <v-col cols="12" md="4">

        <v-card class="pa-3">

          <div class="text-h6 mb-3">
            Cholesterol vs Risk
          </div>

          <img
            :src="`http://127.0.0.1:8000/artifacts/${cholesterolPlot}`"
            style="width:100%; cursor:pointer"
            @click="
              selectedImage=`http://127.0.0.1:8000/artifacts/${cholesterolPlot}`;
              dialog=true
            "
          >

        </v-card>

      </v-col>

      <v-col cols="12" md="4">

        <v-card class="pa-3">

          <div class="text-h6 mb-3">
            Correlation Heatmap
          </div>

          <img
            :src="`http://127.0.0.1:8000/artifacts/${corrPlot}`"
            style="width:100%; cursor:pointer"
            @click="
              selectedImage=`http://127.0.0.1:8000/artifacts/${corrPlot}`;
              dialog=true
            "
          >

        </v-card>

      </v-col>

    </v-row>

    <v-dialog
      v-model="dialog"
      max-width="56%"
    >

      <v-card>

        <v-img
          :src="selectedImage"
          contain
        />

      </v-card>

    </v-dialog>

  </v-container>

</v-window-item>


            <v-window-item value="pred">
  <v-card class="pa-4 mb-4">

    <v-row>

      <v-col cols="12" md="6">
        <v-text-field v-model="form.age" label="Age" />
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
          label="Resting BP"
          :error="form.resting_bp > highRisk.resting_bp"
          :hint="form.resting_bp > highRisk.resting_bp ? 'High BP ⚠️' : ''"
          persistent-hint
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-text-field
          v-model="form.cholesterol"
          label="Cholesterol"
          :error="form.cholesterol > highRisk.cholesterol"
          :hint="form.cholesterol > highRisk.cholesterol ? 'High cholesterol ⚠️' : ''"
          persistent-hint
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-text-field v-model="form.max_heart_rate" label="Max Heart Rate" />
      </v-col>

      <v-col cols="12" md="6">
        <v-text-field
          v-model="form.bmi"
          label="BMI"
          :error="form.bmi > highRisk.bmi"
          :hint="form.bmi > highRisk.bmi ? 'High BMI ⚠️' : ''"
          persistent-hint
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-text-field v-model="form.stress_level" label="Stress Level" />
      </v-col>

      <v-col cols="12" md="6">
        <v-select
          v-model="form.smoking_status"
          :items="['never','former','current']"
          label="Smoking Status"
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-switch
          v-model="form.diabetes"
          color="red"
          :label="form.diabetes ? 'Diabetes: YES' : 'Diabetes: NO'"
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-switch
          v-model="form.family_history"
          color="red"
          :label="form.family_history ? 'Family history: YES' : 'Family history: NO'"
        />
      </v-col>

    </v-row>

    <v-btn color="red" class="mt-2" @click="predictRisk">
      Predict
    </v-btn>

  </v-card>

  <v-card
    v-if="result"
    class="mt-6 pa-4"
    :color="result.risk.includes('High')
      ? 'red-lighten-2'
      : result.risk.includes('Medium')
        ? 'orange-lighten-2'
        : 'green-lighten-2'"
  >
    <div class="text-h6">Prediction Result</div>

    <div class="text-h5 mt-2">
      {{ result.risk }}
    </div>

    <div class="mt-2">
      Final score: {{ result.final_score.toFixed(2) }}
    </div>

    <div>
      RF: {{ result.rf_pred.toFixed(2) }} | DL: {{ result.dl_pred.toFixed(2) }}
    </div>
  </v-card>

  <v-card v-if="explanation.length" class="mt-4 pa-4">
    <div class="text-h6">Why is this a risk?</div>

    <v-chip
      v-for="(r, i) in explanation"
      :key="i"
      class="ma-1"
      color="red"
      variant="flat"
    >
      {{ r }}
    </v-chip>
  </v-card>

  
  <div class="mt-6">
    <canvas ref="chartRef"></canvas>
  </div>

</v-window-item>

        </v-window>

    </v-card>

</v-container>

</template>

<script setup>

import { ref, onMounted, nextTick, computed } from "vue"
import api from "../api/api"
import { Chart, ArcElement, Tooltip, Legend, DoughnutController } from "chart.js"

Chart.register(ArcElement, Tooltip, Legend, DoughnutController)

const chartRef = ref(null)
let chartInstance = null

const explanation = computed(() => {
  const reasons = []

  if (form.value.cholesterol > 240) reasons.push("High cholesterol")
  if (form.value.bmi > 30) reasons.push("High BMI")
  if (form.value.resting_bp > 140) reasons.push("High blood pressure")
  if (form.value.diabetes) reasons.push("Diabetes present")
  if (form.value.family_history) reasons.push("Family history")

  return reasons
})

const highRisk = {
  cholesterol: 240,
  resting_bp: 140,
  bmi: 30,
}

function renderChart(score) {
  if (!chartRef.value) return

  const ctx = chartRef.value.getContext("2d")

  if (chartInstance) {
    chartInstance.destroy()
  }

  chartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Risk", "Safe"],
      datasets: [
        {
          data: [score, 1 - score],
          backgroundColor: ["#e53935", "#43a047"]
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  })
}
const form = ref({
  age: 50,
  gender: "male",
  resting_bp: 120,
  cholesterol: 200,
  max_heart_rate: 150,
  bmi: 25,
  stress_level: 5,
  smoking_status: "never",
  diabetes: 0,
  family_history: 0
})

const result = ref(null)

async function predictRisk() {
  try {
    const response = await api.post("/predict", form.value)

    result.value = response.data

    await nextTick()

    renderChart(response.data.final_score)

  } catch (error) {
    console.log(error)
  }
}
const kpis = ref({})
const metrics = ref({})
const tab = ref("eda1")
const plots = ref([]);
const agePlot = ref("");
const cholesterolPlot = ref("");
const corrPlot = ref("");
const dialog = ref(false)
const selectedImage = ref("")

async function loadPlots() {
  const res = await api.get("/plots");
  plots.value = res.data.plots;

  agePlot.value = plots.value.find(p =>
    p.includes("age")
  );

  cholesterolPlot.value = plots.value.find(p =>
    p.includes("cholesterol")
  );

  corrPlot.value = plots.value.find(p =>
    p.includes("correlation")
  );
}

async function loadKpis() {

    try {

        const kpiResponse = await api.get("/kpis")
        const metricResponse = await api.get("/metrics")

        kpis.value = kpiResponse.data
        metrics.value = metricResponse.data

    }

    catch (error) {

        console.log(error)

    }

}

onMounted(() => {
  loadKpis();
  loadPlots();
});

</script>