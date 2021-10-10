<template>
    <Splitter>
        <SplitterPanel :size="20" :min-size="10" style="background-color: #f6f6f6; overflow-y: scroll">
            <OMEXTree />

            <div class="p-ml-2 p-mt-4 menuheader">SEARCH</div>
            <InputText
                placeholder="Search"
                type="text"
                style="height: 35px; width: 100%"
                v-if="['report', 'Report'].includes($route.name)"
                @input="updateSearchQuery"
            />

            <div class="p-ml-2 p-mt-4 menuheader">FROG RESULTS</div>
        </SplitterPanel>
        <SplitterPanel
            class="panel p-p-2"
            :size="80"
            :min-size="40"
            style="background-color: white"
        >
            <div>FROG Report Tables</div>
        </SplitterPanel>
    </Splitter>
</template>

<script lang="ts">
import store from "@/store/index";
import { defineComponent } from "vue";

import ComponentMenu from "@/components/layout/ComponentMenu.vue";
import OMEXTree from "@/components/layout/OMEXTree.vue";

/**
 * Component to hold all components to show the generated report.
 */
export default defineComponent({
    components: {
        OMEXTree,
    },

    computed: {
        coreComponents(): Array<Record<string, unknown>> {
            return store.getters.reportBasics;
        },
    },
    methods: {
        /**
         * Updates the searchQuery in Vuex state/localStorage to the currently
         * searched string in the search box.
         */
        updateSearchQuery(e: Event): void {
            store.dispatch("updateSearchQuery", (e.target as HTMLInputElement).value);
        },
    },
});
</script>

<style lang="scss">
@import "@/assets/styles/scss/Menu.scss";
.panel {
    overflow-y: scroll;
    //overflow-x: scroll;
    //height: 100%;
    width: 100%;
}
</style>
