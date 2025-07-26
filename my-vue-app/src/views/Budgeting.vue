<script setup>
import { ref, onMounted, inject } from 'vue'
import Envelopes from '../components/Envelopes.vue'
import { useBudgetStore } from '../stores/budget'

const total_budget = ref(0)
const budgetStore = useBudgetStore()
const loading = ref(false)
const envelopesRefs = ref({})

// Inject toast functionality
const showToast = inject('showToast')

// For creating a new envelope
const newEnvelopeName = ref('')
const newEnvelopeBudget = ref(0)
const showEnvelopeForm = ref({}) // Track which budget's envelope form is open
const showCreateForm = ref(false) // Track if create budget form is visible

// Fetch all budgets from backend
async function get_budget() {
    loading.value = true
    try {
        const res = await fetch("http://127.0.0.1:8000/api/budget/load")
        const data = await res.json()
        budgetStore.set_budgets(data)
    } catch (err) {
        showToast("Failed to load budgets. Please try again.", "error")
        console.error(err)
    } finally {
        loading.value = false
    }
}

// Create a new budget
async function create_budget(){
    if (!total_budget.value || total_budget.value <= 0) {
        showToast("Please enter a valid budget amount.", "error")
        return
    }

    loading.value = true
    try {
        const res = await fetch("http://127.0.0.1:8000/api/budget/create", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ total_budget: total_budget.value})
        });
        await res.json()
        await get_budget()
        total_budget.value = 0 // Reset form
        showCreateForm.value = false // Hide form
        showToast("Budget created successfully!", "success")
    } catch (err) {
        showToast("Failed to create budget. Please try again.", "error")
        console.error(err)
    } finally {
        loading.value = false
    }
}

// Delete a budget
async function delete_budget(id) {
    if (!confirm('Are you sure you want to delete this budget? This action cannot be undone.')) {
        return
    }

    loading.value = true
    try {
        await fetch(`http://127.0.0.1:8000/api/budget/delete/${id}`, {
            method: 'DELETE',
        })
        await get_budget()
        showToast("Budget deleted successfully!", "success")
    } catch (err) {
        showToast("Failed to delete budget. Please try again.", "error")
        console.error(err)
    } finally {
        loading.value = false
    }
}

function updateBudget(budget_id, budgetOnEnvelopes) {
    const sourceBudgets = budgetStore.budgets

    // Make a shallow copy to avoid mutating the original array directly
    const updatedBudgets = sourceBudgets.map(budget => {
        if (budget.id === budget_id) {
            return {
                ...budget,
                total_budget: budget.total_budget - budgetOnEnvelopes
            }
        }
        return budget
    })

    budgetStore.set_remaining_budgets(updatedBudgets)
}

// Show/hide the create envelope form for a specific budget
function toggleEnvelopeForm(budget_id) {
    showEnvelopeForm.value[budget_id] = !showEnvelopeForm.value[budget_id]
    // Reset form fields when opening
    if (showEnvelopeForm.value[budget_id]) {
        newEnvelopeName.value = ''
        newEnvelopeBudget.value = 0
    }
}

onMounted(async () => {
    await get_budget()
})
</script>

<template>
  <div class="space-y-8">
    <!-- Page Header with Create Button -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Your Budgets</h1>
      </div>

      <!-- Create Budget Button -->
      <button
        @click="showCreateForm = !showCreateForm"
        class="inline-flex items-center gap-2 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-lg transition shadow-sm"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
        </svg>
        {{ showCreateForm ? 'Cancel' : 'New Budget' }}
      </button>
    </div>

    <!-- Create Budget Form (Conditional) -->
    <div v-if="showCreateForm" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 max-w-md">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-8 h-8 bg-emerald-100 rounded-lg flex items-center justify-center">
          <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
        </div>
        <h2 class="text-lg font-semibold text-gray-900">Create New Budget</h2>
      </div>

      <form @submit.prevent="create_budget" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Budget Amount
          </label>
          <div class="relative">
            <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 font-medium">£</span>
            <input
              v-model="total_budget"
              type="number"
              name="total_budget"
              min="1"
              step="0.01"
              required
              placeholder="0.00"
              class="w-full pl-8 pr-4 py-2.5 border border-gray-200 rounded-lg bg-gray-50 focus:bg-white focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 outline-none transition text-gray-900 font-medium"
            />
          </div>
        </div>

        <div class="flex gap-3">
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 py-2.5 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-400 text-white font-semibold transition flex items-center justify-center gap-2"
          >
            <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Creating...' : 'Create Budget' }}
          </button>
          <button
            type="button"
            @click="showCreateForm = false"
            class="px-4 py-2.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 font-medium transition"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>

    <!-- Budgets Section -->
    <section v-if="!loading">
      <!-- Summary Stats -->
      <div v-if="budgetStore.budgets.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-white rounded-xl p-4 border border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
              </svg>
            </div>
            <div>
              <p class="text-sm text-gray-500">Total Budgets</p>
              <p class="text-xl font-bold text-gray-900">{{ budgetStore.budgets.length }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl p-4 border border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
              </svg>
            </div>
            <div>
              <p class="text-sm text-gray-500">Total Budget</p>
              <p class="text-xl font-bold text-gray-900">
                £{{ budgetStore.budgets.reduce((sum, budget) => sum + budget.total_budget, 0).toFixed(2) }}
              </p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl p-4 border border-gray-100">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
              </svg>
            </div>
            <div>
              <p class="text-sm text-gray-500">Remaining</p>
              <p class="text-xl font-bold text-emerald-600">
                £{{ budgetStore.remaining_budgets.reduce((sum, budget) => sum + budget.total_budget, 0).toFixed(2) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Budgets List -->
      <div v-if="budgetStore.budgets.length > 0" class="space-y-6">
        <div
          v-for="(budget, idx) in budgetStore.budgets"
          :key="budget.id"
          class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition"
        >
          <!-- Budget Header -->
          <div class="p-6 border-b border-gray-50">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">Budget #{{ budget.id }}</h3>
                  <p class="text-sm text-gray-500">Created budget</p>
                </div>
              </div>

              <div class="flex items-center gap-3">
                <!-- Budget Amounts -->
                <div class="text-right">
                  <p class="text-sm text-gray-500">Total</p>
                  <p class="text-lg font-bold text-gray-900">£{{ budget.total_budget.toFixed(2) }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm text-gray-500">Remaining</p>
                  <p class="text-lg font-bold text-emerald-600">£{{ budgetStore.remaining_budgets[idx]?.total_budget.toFixed(2) }}</p>
                </div>

                <!-- Action Buttons -->
                <div class="flex items-center gap-2">
                  <button
                    @click="toggleEnvelopeForm(budget.id)"
                    class="px-4 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg text-sm font-medium transition flex items-center gap-2"
                    title="Create envelope"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
                    </svg>
                    Add Envelope
                  </button>
                  <button
                    @click="delete_budget(budget.id)"
                    class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition"
                    title="Delete budget"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Create Envelope Form -->
          <div v-if="showEnvelopeForm[budget.id]" class="bg-emerald-50 border-b border-emerald-100 p-6">
            <form class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-emerald-700 mb-2">Envelope Name</label>
                  <input
                    v-model="newEnvelopeName"
                    type="text"
                    required
                    placeholder="e.g. Groceries, Entertainment"
                    class="w-full px-4 py-3 border border-emerald-200 rounded-lg bg-white focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 outline-none transition"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-emerald-700 mb-2">Budget Amount</label>
                  <div class="relative">
                    <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 font-medium">£</span>
                    <input
                      v-model.number="newEnvelopeBudget"
                      type="number"
                      min="0.01"
                      step="0.01"
                      required
                      placeholder="0.00"
                      class="w-full pl-8 pr-4 py-3 border border-emerald-200 rounded-lg bg-white focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100 outline-none transition"
                    />
                  </div>
                </div>
              </div>
              <div class="flex gap-3">
                <button
                  type="button"
                  class="flex-1 py-3 px-4 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold transition"
                  @click="envelopesRefs[budget.id].createEnvelope({budget_id: budget.id, newEnvelopeName: newEnvelopeName, newEnvelopeBudget: newEnvelopeBudget})"
                >
                  Create Envelope
                </button>
                <button
                  type="button"
                  @click="toggleEnvelopeForm(budget.id)"
                  class="px-6 py-3 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-600 font-medium transition"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>

          <!-- Envelopes Section -->
          <div class="p-6">
            <Envelopes :budget_id="budget.id" :ref="el => envelopesRefs[budget.id] = el" @update-budget="updateBudget"/>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"/>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-3">No budgets yet</h3>
        <p class="text-gray-500 mb-6 max-w-md mx-auto">
          Create your first budget to start organizing your finances and tracking your spending.
        </p>
        <button
          @click="showCreateForm = true"
          class="inline-flex items-center gap-2 px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-lg transition shadow-sm"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
          </svg>
          Create Your First Budget
        </button>
      </div>
    </section>

    <!-- Loading State -->
    <div v-else class="text-center py-12">
      <div class="w-16 h-16 border-4 border-emerald-200 border-t-emerald-600 rounded-full animate-spin mx-auto mb-4"></div>
      <p class="text-gray-500">Loading your budgets...</p>
    </div>
  </div>
</template>