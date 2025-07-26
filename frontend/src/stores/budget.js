import { defineStore } from 'pinia'

export const useBudgetStore = defineStore('budget', {
        state : () => ({budgets : [], remaining_budgets : []}),
        actions : {
            set_budgets(budgets) {
                this.budgets = budgets
            },
            set_remaining_budgets(remaining_budgets) {
                this.remaining_budgets = remaining_budgets
            }
        }
    }
)