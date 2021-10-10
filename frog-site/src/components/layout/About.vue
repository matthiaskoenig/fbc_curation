<template>
    <div class="p-px-2">
        <ScrollPanel style="width: 100%">
            <h1>About</h1>
            <Panel header="FROG">
                <div class="p-d-flex content">
                    <a href="https://runfrog.de" class="image">
                        <img
                            src="@/assets/images/frog-192x192.png"
                            height="50"
                        />
                    </a>
                    <p>
                        The objective of the FROG analysis is to provide reproducible
                        output for FBC curation.

                        If you use <a href="https://runfrog.de">https://runfrog.de</a> in your work cite<br />
                        <a
                            href="https://zenodo.org/badge/latestdoi/3708271"
                            target="_blank"
                            rel="nofollow"
                            ><img
                                class="p-pt-1"
                                alt="Zenodo DOI"
                                src="https://camo.githubusercontent.com/332b1f7dd91e445f074084a39ed733363fa353b257d9e526d489c88dab025172/68747470733a2f2f7a656e6f646f2e6f72672f62616467652f35353935323834372e737667"
                                data-canonical-src="https://zenodo.org/badge/3708271.svg"
                                style="max-width: 100%"
                        /></a>
                    </p>
                </div>
            </Panel>
            <!-- Team -->
            <Panel header="Team">
                <div class="p-d-flex content">
                    <a href="https://livermetabolism.com" class="image">
                        <img src="@/assets/images/people/koenig.png" height="50" />
                    </a>
                    <p>
                        <a href="https://livermetabolism.com" target="_blank"
                            >Dr. Matthias König</a
                        >, Humboldt University, Berlin. Matthias König (PhD. in
                        Biophysics) leads an independent
                        <a href="https://livermetabolism.com" target="_blank"
                            >junior research group</a
                        >
                        for Systems Biology and Systems Medicine of the liver with focus
                        on metabolic research at the Humboldt University Berlin. He has
                        been actively involved in the development of SBML, SED-ML and
                        software supporting these standards.
                    </p>
                </div>
            </Panel>
            <!-- Funding -->
            <Panel header="Funding">
                <div class="p-d-flex content">
                    <p>
                        Matthias König is supported by the Federal Ministry of Education
                        and Research (BMBF, Germany) within the research network Systems
                        Medicine of the Liver (<a
                            href="https://lisym.org/"
                            target="_blank"
                            >LiSyM</a
                        >, grant number 031L0054).
                    </p>
                </div>
                <div class="p-d-flex content">
                    <p>
                        Matthias König is supported by the German Research Foundation
                        (DFG) within the Research Unit Programme FOR 5151 "<a
                            href="https://qualiperf.de"
                            >QuaLiPerF</a
                        >
                        (Quantifying Liver Perfusion-Function Relationship in Complex
                        Resection - A Systems Medicine Approach)" by grant number
                        436883643.
                    </p>
                </div>
            </Panel>
        </ScrollPanel>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "About",
});
</script>

<style lang="scss" scoped>
.image {
    max-width: 100%;
    height: auto;
    margin: auto 30px;
}

.content {
    text-align: justify;
}

.img-circle {
    border-radius: 50%;
}
</style>
