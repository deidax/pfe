import Api from './server'
import AuthHeader from './authHeader'


const RUN_CRAWLER_END_POINT = "/crawler/"
const CRAWLER_END_POINT = "/crawler_manager"

export default{

    async createCrawler(form){
        return Api.post(CRAWLER_END_POINT, form)
    },

    async runCrawler(id){
        return Api.get(RUN_CRAWLER_END_POINT+id)
    },

    async getAllCrawlers(){
        return Api.get(CRAWLER_END_POINT)
    },


    
}