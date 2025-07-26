<script setup>
import { ref, onMounted, inject } from 'vue'
import AddMoneyModal from './modals/AddMoneyModal.vue'
import SpendMondeyModal from './modals/SpendMondeyModal.vue'
import DeleteEnvelopeModal from './modals/DeleteEnvelopeModal.vue'

const props = defineProps({
    budget_id: {
        type: Number,
        required: true
    }
})

const emit = defineEmits(['update-budget'])

// Inject toast functionality
const showToast = inject('showToast')

// Holds the list of envelopes for this budget
const envelopes = ref([])
const loading = ref(false)

const addMoneyModal = ref(null)
const spendMoneyModal = ref(null)
const deleteEnvelopeModal = ref(null)

const budget = ref(0)

function getEnvelopesBudget() {
    budget.value = 0
    for (const envelope of envelopes.value) {
        budget.value += envelope.anvelope_budget
    }
}

// Fetch envelopes for the given budget_id when component mounts
async function fetchEnvelopes() {
    loading.value = true
    try {
        const res = await fetch(`http://127.0.0.1:8000/api/anvelopes/load/${props.budget_id}`)
        const data = await res.json()
        envelopes.value = data
        getEnvelopesBudget()
        emit('update-budget', props.budget_id, budget.value)
    } catch (err) {
        showToast("Failed to load envelopes. Please try again.", "error")
        console.error(err)
    } finally {
        loading.value = false
    }
}

const addMoney = (data) => {
    envelopes.value.find(envelope => envelope.id === data.envelope_id).anvelope_budget += data.amount
    getEnvelopesBudget()
    emit('update-budget', props.budget_id, budget.value)
    showToast(`Added £${data.amount.toFixed(2)} to envelope`, "success")
}

const spendMoney = (data) => {
    envelopes.value.find(envelope => envelope.id === data.envelope_id).anvelope_budget -= data.amount
    getEnvelopesBudget()
    emit('update-budget', props.budget_id, budget.value)
    showToast(`Spent £${data.amount.toFixed(2)} from envelope`, "info")
}

const deleteEnvelope = (data) => {
    envelopes.value = envelopes.value.filter(envelope => envelope.id !== data.envelope_id)
    getEnvelopesBudget()
    emit('update-budget', props.budget_id, budget.value)
    showToast("Envelope deleted successfully!", "success")
}

// Create a new envelope for a budget
const createEnvelope = async (data) => {
    const { budget_id, newEnvelopeName, newEnvelopeBudget } = data
    if (!newEnvelopeName || newEnvelopeBudget <= 0) {
        showToast("Please enter a valid envelope name and budget.", "error")
        return
    }

    loading.value = true
    try {
        const res = await fetch(`http://127.0.0.1:8000/api/anvelopes/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                budget_id: budget_id,
                anvelope_name: newEnvelopeName,
                anvelope_budget: newEnvelopeBudget
            })
        })
        const data = await res.json()
        envelopes.value.push({
            id: data,
            anvelope_name: newEnvelopeName,
            anvelope_budget: newEnvelopeBudget
        })

        getEnvelopesBudget()
        emit('update-budget', budget_id, budget.value)
        showToast(`Envelope "${newEnvelopeName}" created successfully!`, "success")
    } catch (err) {
        showToast("Failed to create envelope. Please try again.", "error")
        console.error(err)
    } finally {
        loading.value = false
    }
}

defineExpose({
    createEnvelope
})

onMounted(() => {
    fetchEnvelopes()
})
</script>

<template>
  <div>
    <!-- Section Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">Envelopes</h3>
        <p class="text-sm text-gray-500">
          {{ envelopes.length }} envelope{{ envelopes.length !== 1 ? 's' : '' }} • £{{ budget.toFixed(2) }} allocated
        </p>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-8">
      <div class="w-8 h-8 border-2 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mx-auto mb-3"></div>
      <p class="text-sm text-gray-500">Loading envelopes...</p>
    </div>

    <!-- Envelopes Grid -->
    <div v-else-if="envelopes.length > 0" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="envelope in envelopes"
        :key="envelope.id"
        class="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200 group"
      >
        <!-- Envelope Header -->
        <div class="flex items-start justify-between mb-4">
          <div class="flex-1">
            <h4 class="text-lg font-semibold text-gray-900 mb-1 group-hover:text-emerald-700 transition">
              {{ envelope.anvelope_name }}
            </h4>
            <div class="flex items-center gap-2">
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                #{{ envelope.id }}
              </span>
              <span class="text-xs text-gray-400">Envelope</span>
            </div>
          </div>
        </div>

        <!-- Amount Display -->
        <div class="mb-6">
          <div class="flex items-baseline gap-1">
            <span class="text-2xl font-bold text-emerald-600">£{{ envelope.anvelope_budget.toFixed(2) }}</span>
            <span class="text-sm text-gray-400 font-medium">available</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="space-y-2">
          <!-- Add Money Button -->
          <button
            class="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg font-medium transition-colors duration-150"
            @click="addMoneyModal.openAddMoneyModal(envelope.id)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
            </svg>
            Add Money
          </button>

          <!-- Spend Money Button -->
          <button
            class="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-amber-50 hover:bg-amber-100 text-amber-700 rounded-lg font-medium transition-colors duration-150"
            @click="spendMoneyModal.openSpendMoneyModal(envelope.id)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4"/>
            </svg>
            Spend Money
          </button>

          <!-- Delete Button -->
          <button
            class="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg font-medium transition-colors duration-150"
            @click="deleteEnvelopeModal.openDeleteModal(envelope.id)"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
            Delete Envelope
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
        </svg>
      </div>
      <h3 class="text-lg font-semibold text-gray-900 mb-2">No envelopes yet</h3>
      <p class="text-gray-500 mb-4">Create your first envelope to start organizing your budget</p>
    </div>

    <!-- Modals -->
    <AddMoneyModal ref="addMoneyModal" @add-money="addMoney" />
    <SpendMondeyModal ref="spendMoneyModal" @spend-money="spendMoney" />
    <DeleteEnvelopeModal ref="deleteEnvelopeModal" @delete-envelope="deleteEnvelope" />
  </div>
</template>