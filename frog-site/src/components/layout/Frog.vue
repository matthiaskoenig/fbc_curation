<template>
    <div class="p-p-4">
    <ProgressBar v-if="running" class="p-my-5" mode="indeterminate" style="height: 0.5em" />
        {{ error }}
    <h1>FROG report</h1>
    <h2>{{ $route.params.id }}</h2>

    <strong>Status</strong>: <Tag :value="status"></Tag>
        <div>
            <code style="font-size: x-small">{{ result }}</code>
        </div>
    </div>
</template>

<script lang="ts">
import store, {VUE_APP_APIURL} from "@/store/index";
import { defineComponent } from "vue";
import axios from "axios";
import Tag from "primevue/tag";


export default defineComponent({
    components: {},

    computed: {
        task_id(){
            return this.$route.params.id;
        },
        // manifest(){
        //     return this.data.result.manifest;
        // },
        // frogs(){
        //     return this.data.result.frogs;
        // },
    },
    data() {
        return {
            error: null,
            result: {
                manifest: null,
                frogs: null,
            },
            status: "undefined",
            running: true,
        };
    },
    methods: {
        queryTaskStatus() {
            this.running = true;

            const url = VUE_APP_APIURL + "/api/task/status/" + this.task_id;
            console.log(url)
            axios.get(url)
                .then((res) => {
                    console.log(res);
                    this.status = res.data.task_status;
                    this.result = res.data.task_result;
                })
                .catch((error) => {
                    console.log(error);
                    this.error = error
                });
            if (this.status === "SUCCESS"){
                this.running = false;
                return null;
            }
            if (this.task_id === "undefined"){
                this.running = false;
                this.status = "NO_TASK_ID"
                return null;
            }


            setTimeout(() => {
              this.queryTaskStatus();
            }, 5000);
        },
    },
    mounted() {
        this.queryTaskStatus();
  }
});
</script>

<style lang="scss">
</style>
