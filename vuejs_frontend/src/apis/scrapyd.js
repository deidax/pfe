import Scrapyd from './scrapyd_server'
import Api from './server'


const SCRAPYD_LIST_JOBS_END_POINT = "/listjobs"
const SCRAPYD_CANCEL_JOB = "/crawler_cancel_process"

export default{

    async getRuningJobs(form){
        return Api.post(SCRAPYD_LIST_JOBS_END_POINT, form)
    },

    async cancelRunningJob(form){
        return Api.post(SCRAPYD_CANCEL_JOB, form)
    }

}