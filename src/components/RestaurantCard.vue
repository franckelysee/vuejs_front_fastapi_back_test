<script>
export default {
    name:"RestaurantCard",
}
</script>

<template>
<div class="restaurant--card">
    <div class="restaurant--image flex">
        <img src="https://cn-geo1.uber.com/image-proc/resize/eats/format=webp/width=550/height=440/quality=70/srcb64=aHR0cHM6Ly9kMXJhbHNvZ25qbmczNy5jbG91ZGZyb250Lm5ldC8zNzg4MDJiMC1jNTI4LTQ4MjktYjBiNS0wY2M2NDBkZjYzY2QuanBlZw==" alt="" srcset="">

    </div>
    <div class="restaurant__info">
        <div class="top flex">
            <p class="name">
                Subway
            </p>
            <p class="not">4.5</p>
        </div>
        <p class="time">25 - 35 <span>min  <sup>.€€</sup></span></p>
    </div>
</div>
</template>

<style>
.restaurant--card {
    width: 32%;
    height: 30vh;

    p {
        margin: 0px;
    }
    .restaurant--image {
        height: 70%;
        background-size: cover;
        background-position: center;

        img{
            height: 100%;
            width: 100%;
        }
    }
    .restaurant__info{
        
        .top{
            padding-top: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;

            .not{
                background: rgba(122, 243, 243, 0.527);
                border-radius: 50%;
                padding: 4px;
                color: rgb(13, 179, 151);
                font-size: 9px;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
            }
        }
        .time{
            color: grey;
            font-size: 12px;
        }
    }
}


</style>
