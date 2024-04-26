<script >
    import RestaurantCard from './RestaurantCard.vue';
    export default{
        name: "RestaurantRow",
        components:{
            RestaurantCard
        }
    }
</script>

<template>
    <div class="restaurant--row">
        <div class="title">
            <h2>Nos Restaurant</h2>
        </div>
        <div class="restaurant__cards">
            <restaurant-card v-for="(card, index) in 3"></restaurant-card>
        </div>
    </div>
</template>

<style >
.restaurant--row{
    .title{
        font-size: 30px;
        font-family: 'Times New Roman', Times, serif;
        font-weight: bold;
    }
    .restaurant__cards{
        display: flex;
        justify-content: space-between;
        align-items: center;
        

    }
}
</style>