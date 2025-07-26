<script setup>
import { ref, nextTick, inject } from 'vue'

// Inject toast functionality
const showToast = inject('showToast')

const envelope_id = ref(0)
const spendAmount = ref(0)
const showSpendModal = ref(false)
const loading = ref(false)

const emit = defineEmits(['spend-money'])

const openSpendMoneyModal = async (envelopeId) => {
    envelope_id.value = envelopeId
    showSpendModal.value = true
    spendAmount.value = 0

    // Wait for DOM to update, then focus the input
    await nextTick()
    const input = document.getElementById('spend-money-input')
    if (input) {
        input.focus()
    }
}

const closeSpendMoneyModal = () => {
    showSpendModal.value = false
    spendAmount.value = 0
    loading.value = false
}

// Submit the spend money form
async function submitSpendMoney() {
    if (!envelope_id.value || spendAmount.value <= 0) {
        showToast("Please enter a valid amount.", "error")
        return
    }

    loading.value = true
    try {
        // Call backend to spend money
        await fetch(`http://127.0.0.1:8000/api/anvelopes/spend_money/${envelope_id.value}/${spendAmount.value}`, {
            method: 'POST'
        })
        // Refresh envelopes after spending money
        emit('spend-money', {
            envelope_id: envelope_id.value,
            amount: spendAmount.value
        })
        closeSpendMoneyModal()
    } catch (err) {
        showToast("Failed to spend money. Please try again.", "error")
        console.error(err)
    } finally {
        loading.value = false
    }
}

const validateAmount = () => {
    if (spendAmount.value <= 0) {
        showToast("Please enter a valid amount greater than 0.", "error")
    }
}

defineExpose({
    openSpendMoneyModal
})
</script>

<template>
  <!-- Modal Backdrop -->
  <div v-if="showSpendModal" class="fixed inset-0 flex items-center justify-center bg-black/50 z-50 p-4">
    <!-- Modal Card -->
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md border border-gray-100 relative animate-in fade-in duration-200">
      <!-- Modal Header -->
      <div class="p-6 border-b border-gray-100">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 bg-amber-100 rounded-xl flex items-center justify-center">
            <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4"/>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-gray-900">Spend Money</h3>
            <p class="text-sm text-gray-500">Record an expense from this envelope</p>
          </div>
        </div>
      </div>

      <!-- Modal Body -->
      <div class="p-6">
        <form @submit.prevent="submitSpendMoney" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              Amount Spent
            </label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 font-medium">£</span>
              <input
                id="spend-money-input"
                v-model.number="spendAmount"
                type="number"
                min="0.01"
                step="0.01"
                class="w-full pl-8 pr-4 py-3 border border-gray-200 rounded-lg bg-gray-50 focus:bg-white focus:border-amber-400 focus:ring-2 focus:ring-amber-100 outline-none transition text-gray-900 font-medium"
                required
                placeholder="0.00"
                @input="validateAmount"
              />
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-2">
            <button
              type="button"
              @click="closeSpendMoneyModal"
              class="flex-1 py-3 px-4 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="loading || !spendAmount || spendAmount <= 0"
              class="flex-1 py-3 px-4 rounded-lg bg-amber-600 hover:bg-amber-700 disabled:bg-amber-400 text-white font-semibold transition flex items-center justify-center gap-2"
            >
              <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Recording...' : 'Record Expense' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>