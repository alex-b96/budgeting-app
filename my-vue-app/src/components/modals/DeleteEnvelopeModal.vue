<script setup>
import { ref, inject } from 'vue'

// Inject toast functionality
const showToast = inject('showToast')

const envelope_id = ref(0)
const showDeleteModal = ref(false)
const loading = ref(false)

const emit = defineEmits(['delete-envelope'])

const openDeleteModal = (envelopeId) => {
    envelope_id.value = envelopeId
    showDeleteModal.value = true
}

const closeDeleteModal = () => {
    showDeleteModal.value = false
    envelope_id.value = 0
    loading.value = false
}

// Submit the delete envelope form
async function submitDeleteEnvelope() {
    if (!envelope_id.value) {
        showToast("Invalid envelope ID.", "error")
        return
    }

    loading.value = true
    try {
        // Call backend to delete envelope
        await fetch(`http://127.0.0.1:8000/api/anvelopes/delete/${envelope_id.value}`, {
            method: 'DELETE'
        })
        // Refresh envelopes after deleting
        emit('delete-envelope', {
            envelope_id: envelope_id.value
        })
        closeDeleteModal()
    } catch (err) {
        showToast("Failed to delete envelope. Please try again.", "error")
        console.error(err)
    } finally {
        loading.value = false
    }
}

defineExpose({
    openDeleteModal
})
</script>

<template>
  <!-- Modal Backdrop -->
  <div v-if="showDeleteModal" class="fixed inset-0 flex items-center justify-center bg-black/50 z-50 p-4">
    <!-- Modal Card -->
    <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md border border-gray-100 relative animate-in fade-in duration-200">
      <!-- Modal Header -->
      <div class="p-6 border-b border-gray-100">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 bg-red-100 rounded-xl flex items-center justify-center">
            <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </div>
          <div>
            <h3 class="text-xl font-semibold text-gray-900">Delete Envelope</h3>
            <p class="text-sm text-gray-500">Remove this envelope permanently</p>
          </div>
        </div>
      </div>

      <!-- Modal Body -->
      <div class="p-6">
        <div class="space-y-4">
          <!-- Warning Message -->
          <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
            <div class="flex items-start gap-3">
              <svg class="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
              <div>
                <h4 class="text-sm font-semibold text-red-800 mb-1">Are you sure?</h4>
                <p class="text-sm text-red-700">
                  This action cannot be undone. The envelope and all its data will be permanently deleted.
                </p>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 pt-2">
            <button
              type="button"
              @click="closeDeleteModal"
              class="flex-1 py-3 px-4 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium transition"
            >
              Cancel
            </button>
            <button
              type="button"
              @click="submitDeleteEnvelope"
              :disabled="loading"
              class="flex-1 py-3 px-4 rounded-lg bg-red-600 hover:bg-red-700 disabled:bg-red-400 text-white font-semibold transition flex items-center justify-center gap-2"
            >
              <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Deleting...' : 'Delete Envelope' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>