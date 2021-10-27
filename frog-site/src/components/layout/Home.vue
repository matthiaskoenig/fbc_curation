<template>
    <div>
        <div class="p-grid">
            <div class="p-col-12 p-lg-6">
                <div>
                    <div class="p-m-3">
                        <submit-options />
                    </div>
                </div>
            </div>
            <div class="p-col-12 p-lg-6">
                <div class="p-m-3">
                    <!--<about />-->
                    <examples />
                    <!--<task-queue />-->
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "@vue/runtime-core";

import Examples from "@/components/layout/Examples.vue";
import SubmitOptions from "@/components/layout/SubmitOptions.vue";
// import About from "@/components/layout/About.vue";
// import About from "@/components/layout/TaskQueue.vue";
//import TaskQueue from "@/components/layout/TaskQueue.vue";

export default defineComponent({
    components: {
        Examples,
        SubmitOptions,
        //About,
    },
});
</script>

<style scoped lang="scss"></style>
