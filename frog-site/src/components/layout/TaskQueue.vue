<template>
    <div>
        <h1>Task Queue</h1>
        <ProgressBar v-if="running" class="p-my-5" mode="indeterminate" style="height: 0.5em" />
        Task Id: {{ task_id }}<br />
        Status: {{ status }}<br />
        <Button class="p-mt-2" type="button" @click="submitTask($event)"
            >Submit Task</Button>
        <!--<Button class="p-mt-2" type="button" @click="queryTaskStatus($event)"
            >Query Status</Button>-->
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { FilterMatchMode, FilterOperator } from "primevue/api";
import store, { VUE_APP_APIURL } from "@/store";
import axios from "axios";
import { checkAPIResponse } from "@/helpers/additionalInfoUtils";

export default defineComponent({
    name: "TaskQueue",
    data() {
        return {
            response: {},
            task_id: "-",
            status: "-",
            running: false,
        };
    },
    methods: {
        submitTask() {
            const url = VUE_APP_APIURL + "/tasks/";
            //const response = await axios.get(url);
            this.task_id = "-";
            this.status = "-";
            axios
                .post(url,
                    {
                        type: 1,
                    },
                )
                .then((res) => {
                    console.log(res);
                    this.task_id = res.data.task_id;
                })
                .catch((error) => {
                    console.log(error);
                });
            this.running = true;

            this.queryTaskStatus();
        },
        queryTaskStatus() {
            const url = VUE_APP_APIURL + "/tasks/" + this.task_id;
            //const response = await axios.get(url);
            axios.get(url)
                .then((res) => {
                    console.log(res);
                    this.status = res.data.task_status;
                    this.response = res
                })
                .catch((error) => {
                    console.log(error);
                });
            if (this.status === "SUCCESS"){
                this.running = false
                return null;
            }

            setTimeout(() => {
              this.queryTaskStatus();
            }, 1000);
        },
    },
});
</script>

<style lang="scss" scoped></style>
