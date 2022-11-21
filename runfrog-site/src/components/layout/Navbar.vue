<template>
    <menubar :model="items">
        <template #start>
            <div class="p-d-flex">
                <router-link to="/">
                    <img
                        to="/"
                        alt="logo"
                        src="@/assets/images/frog_icon_mirrored.svg"
                        height="35"
                    />
                </router-link>

                <router-link to="/">
                    <span class="frog p-mx-3" style="color: black">Run FROG</span>
                </router-link>
            </div>
        </template>
    </menubar>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import store, {VUE_APP_APIURL, VUE_APP_BASEURL, VUE_APP_FLOWERURL} from "@/store";

/**
 * Navbar component for providing main links in the application
 */
export default defineComponent({
    data() {
        return {
            items: [
                {
                    label: "Home",
                    icon: "pi pi-fw pi-home",
                    to: "/",
                },
                {
                    label: "REST API",
                    icon: "pi pi-fw pi-sitemap",
                    url: VUE_APP_APIURL + "/docs",
                },
                {
                    label: "Dashboard",
                    icon: "pi pi-fw pi-desktop",
                    url: VUE_APP_FLOWERURL + "/flower/",
                },
                {
                    label: "Report issue",
                    icon: "pi pi-fw pi-pencil",
                    url: "https://github.com/matthiaskoenig/fbc_curation/issues/new/choose",
                },
                {
                    label: "Documentation",
                    icon: "pi pi-fw pi-info-circle",
                    url: "https://fbc-curation.readthedocs.io",
                },
                {
                    label: "Code",
                    icon: "pi pi-fw pi-github",
                    url: "https://github.com/matthiaskoenig/fbc_curation",
                },
            ],
        };
    },
});
</script>

<style lang="scss" scoped>
.frog {
    font-family: "Roboto Slab", serif;
    font-size: 30px;
}

.image-rotate {
    position: relative;
    top: 50%;
    left: 50%;
    width: 120px;
    height: 120px;
    margin: -60px 0 0 -60px;
    -webkit-animation: spin 4s linear infinite;
    -moz-animation: spin 4s linear infinite;
    animation: spin 4s linear infinite;
}
@-moz-keyframes spin {
    100% {
        -moz-transform: rotate(360deg);
    }
}
@-webkit-keyframes spin {
    100% {
        -webkit-transform: rotate(360deg);
    }
}
@keyframes spin {
    100% {
        -webkit-transform: rotate(360deg);
        transform: rotate(360deg);
    }
}
</style>
