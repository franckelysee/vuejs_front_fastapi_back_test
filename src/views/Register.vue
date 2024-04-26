<script setup>
    import { ref } from 'vue';
    import axios from 'axios';


    const credentials = ref({
        username: "",
        email: "",
        password: "",
        confirm_pass:"",
        address:"",
        phone: ""
    });

    const _state = ref({
        error:"",
        succes:"",
        show:false,
        loading: false,
    });

    function registerSubmit(e){
        const url = axios.defaults.baseURL + "register";
        const data = {
            ...credentials.value,
        };

        _state.value.error = ""
        _state.value.show = false
        _state.value.succes = ""
        _state.value.loading = true

        axios.post(
            url,
            {...data}
        ).then((response)=>{
            console.log("response", response.config.data)
        }).catch((err)=>{
            console.log(err.response.data.detail)
        })
    }

</script>

<template>
    <div class="form_container">
        <form  >
            <div class="main-content">
                <div class="title">
                    <h1>Register</h1>
                </div>
                <div class="inputs">
                    <div>
                        <input type="text" name="name" id="name" v-model="credentials.username"  placeholder="User Name">
                    </div>
                    <div>
                        <input type="text" name="email" id="email" v-model="credentials.email"  placeholder="Email">
                    </div>
                    <div>
                        <textarea name="adresse" id="adresse" cols="30" rows="1" v-model="credentials.address" placeholder="Enter your Adress" ></textarea>
                    </div>
                    <div>
                        <input type="password" name="password" id="password" v-model="credentials.password"  placeholder="password">
                    </div>
                    <div>
                        <input type="password" name="c-pass" id="c-pass" v-model="credentials.confirm_pass"  placeholder="Confirm Password">
                    </div>
                    <div>
                        <input type="text" name="phone" id="phone" v-model="credentials.phone"  placeholder="Phone Number">
                    </div>
                </div>
                <div class="buttons">
                    <Button @click.stop.prevent="registerSubmit">
                        Register
                    </Button>
                    
                </div>
                <div class="sign_In">
                    <span>Already have an account?
                        <RouterLink to="/login" class="sgn_link">Sign In</RouterLink>
                    </span>
                </div>
            </div>
        </form>
    </div>
</template>

<style>
    .form_container{
        margin-top: 10%;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: auto;
        align-items: center;
        width: 500px;
        .error{
            width: 99%;
            padding: 10px;
            border: 1px solid red;
            text-align: center;
            color: red;
            transition: all  2s  ease-in-out;
            box-shadow: 2px 1px 10px 0px #df5050d8;
            display: flex;
            justify-content: center;
            gap: 10px;
            align-items: center;

            .error-svg{
                width: 30px;
                height: 30px;
            }
        }
        .succes{
            width: 500px;
            padding: 10px;
            border: 1px solid #26f8a1;
            text-align: center;
            color: #26f8a1;
            transition: all  2s  ease-in-out;
            box-shadow: 2px 1px 10px 0px #26f8a1;
        }
        form{
            width: 500px;
            align-items: center;
            text-align: center;
            padding-bottom: 20px;
            padding-top: 20px;
            box-shadow: 2px 1px 10px 0px #508edfd8;

            .main-content{
                display: flex;
                flex-direction: column;
                gap: 10px;

                .title{
                    font-size: 24px;
                    text-transform:uppercase ;
                    color: #508edfd8;
                }

                .inputs{
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                    input,textarea{
                        border-bottom: 1px solid #508edfd8;
                        padding: 5px;
                        padding-left: 10px;
                        outline: none;  
                        width: 80%;                      
                    }
                }
                .buttons{
                    margin-top: 10px;
                    display: flex;
                    justify-content: center;
                    button{
                        box-shadow: 1px 1px 3px 1px #012657d8;
                        width: 50%;
                        padding: 5px;
                        color: white;
                        background: #5d88c2d8;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 10px;
                        .loading_svg{
                            width: 20px;
                        }
                    }
                    button:hover{
                        box-shadow: 1px 1px 3px 1px #508edfd8;
                        background: #02316ed8;
                    }
                }
                .sign_In{
                    font-size: 15px;
                    color: grey;
                    padding: 10px;
                    
                    .sgn_link{
                        color: #508edfd8;
                    }
                }
            }
        }
    }
</style>