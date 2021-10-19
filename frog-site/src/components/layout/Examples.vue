<template>
    <div class="p-p-2">
        <TabView>
            <TabPanel>
                <template #header>
                    <i class="pi pi-list p-mr-2"></i>
                    <span>Examples</span>
                    <InputText
                        v-model="filters['global'].value"
                        class="searchBar p-ml-5"
                        placeholder="Search examples"
                    />
                </template>
                <DataTable
                    :value="examples"
                    :paginator="true"
                    :rows="10"
                    :rowsPerPageOptions="[10, 25, 50]"
                    v-model:filters="filters"
                    filterDisplay="menu"
                    sortMode="multiple"
                    v-if="examples.length > 0"
                    style="font-size: 12px"
                    class="p-datatable-sbml"
                    :globalFilterFields="['global', 'searchUtilField']"
                    responsiveLayout="scroll"
                    :rowHover="true"
                    @row-click="getExample($event.data.id)"
                >
                    <Column sortable style="width: fit-content" field="id" header="id">
                        <template #body="props">
                            <strong>{{ props.data.id }}</strong>
                        </template>
                    </Column>
                    <Column
                        sortable
                        style="width: fit-content"
                        field="description"
                        header="description"
                    >
                        <template #body="props">
                            {{ props.data.description }}
                        </template>
                    </Column>
                </DataTable>
                <loading parent="example" message="Loading FROG examples" />
            </TabPanel>
        </TabView>
    </div>
</template>

<script lang="ts">
import store from "@/store/index";
import { defineComponent } from "@vue/runtime-core";
import { FilterMatchMode, FilterOperator } from "primevue/api";

/* Components */
import Loading from "@/components/layout/Loading.vue";

/**
 * Component to display list of all example models fetched from API.
 */
export default defineComponent({
    components: {
        Loading,
    },
    data() {
        return {
            filters: {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
                searchUtilField: {
                    operator: FilterOperator.AND,
                    constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }],
                },
            },
        };
    },
    created(): void {
        store.dispatch("fetchExamples");
    },

    methods: {
        getExample(exampleId: string): void {
            const payload = {
                exampleId: exampleId,
            };
            store.dispatch("fetchExampleReport", payload);
        },
    },

    computed: {
        /**
         * Reactively returns the list of examples from Vuex state/localStorage.
         */
        examples(): Array<Record<string, unknown>> {
            return store.state.examples;
        },

        /**
         * Reactively returns the loading status of the example(s) from Vuex state/localStorage.
         */
        loading(): boolean {
            return store.state.exampleLoading;
        },
    },
});
</script>

<style lang="scss" scoped></style>
