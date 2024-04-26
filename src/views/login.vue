<script setup>
    import {ref} from "vue";
    import axios from "axios";
    import { useRoute, useRouter } from "vue-router";
    import { errorMessages } from "vue/compiler-sfc";

    const credentials = ref({
        email: "",
        password: "",
    });
    const _state = ref({
        error:"",
        succes:"",
        show:false,
        loading: false,
    });
    const route = useRoute();
    function loginSubmit(e){

        const url = axios.defaults.baseURL + "auth/login";
        const data={
            ...credentials.value,
        };

        _state.value.error = ""
        _state.value.show = false
        _state.value.succes = ""
        _state.value.loading = true
        axios.post(url,{...data})
        .then((response)=>{
            let data = response;
            let user = data.data.user;
            _state.value.succes = "Log In Sucessfully";
            console.log(user);
            route.query.redirect = "hi"
            console.log("route", route.query.redirect);
            // window.location.href = "/about"
        }).catch((err)=>{
            _state.value.show = true
            console.log("err",err)
            if(err.response.data){
                _state.value.error = err.response.data.user.detail;
            }else{
                _state.value.error = "Unknow error";
            }
        }).finally(()=>{
            _state.value.loading = false
        })
    }
</script>

<template>
    <div class="main_form">
        <div class="form_container">
            <div class="error" v-if="_state.error">
            <svg
                class="error-svg inline w-5 h-5 mr-3"
                fill="currentColor"
                viewBox="0 0 20 20"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clip-rule="evenodd"
                ></path>
            </svg>
                {{ _state.error }}
            </div>

            <div class="succes" v-if="_state.succes">
                {{ _state.succes }}
            </div>
            <form  >
                <div class="main-content">
                    <div class="title">
                        <h1>Login</h1>
                    </div>
                    <div class="inputs">
                        <div>
                            <input type="text" name="email" id="email" v-model="credentials.email" placeholder="Email">
                        </div>
                        <div>
                            <input type="password" name="password" id="password" v-model="credentials.password" placeholder="password">
                        </div>
                    </div>
                    <div class="buttons">
                        <Button @click.stop.prevent="loginSubmit">
                            <svg
                                v-if="_state.loading"
                                aria-hidden="true"
                                role="status"
                                class="loading_svg inline w-4 h-4 mr-3 text-gray-200 animate-spin dark:text-gray-600"
                                viewBox="0 0 100 101"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                                fill="currentColor"
                                />
                                <path
                                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                                fill="#1C64F2"
                                />
                            </svg>
                            Sign In
                        </Button>
                        
                    </div>
                    <div class="sign_In">
                        <span>Don't have an account?
                            <RouterLink to="/register" class="sgn_link">Register here!!</RouterLink>
                        </span>
                    </div>
                </div>
            </form>
        </div>
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
                    input{
                        border-bottom: 1px solid #508edfd8;
                        padding: 5px;
                        outline: none;                        
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