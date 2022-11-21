<template>
    <div>
        <div class="grid">
            <div class="col-12 col-offset-0 md:col-8 md:col-offset-2 ">
                <div>
                    <div class="m-3">
                        <submit-options />
                    </div>
                </div>
                <div class="m-3">
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
