// import state from "../../state";

import Vue from 'vue'

export const SET_CRAWLERS_DATA = (state, crawlers_data) => {
    state.crawlers = crawlers_data;
}



export const SET_OTHER_ERRORS = (state,value) => {
    state.other_errors.push(value)
}

export const CLEAR_OTHER_ERRORS = (state) => {
    state.other_errors.length = 0
}

export const SET_LOADING = (state,value) => {
    state.loading = value
}

export const SET_LOADING_TO_SCRAPYD = (state, value) => {
    state.loading_scrapyd = value
}

export const SET_RUNNING_CRAWLER = (state, value) => {
    state.running_crawler = value
}

export const SET_RUNNING_CRAWLER_TASK_ID = (state, value) => {
    state.running_crawler_task_id = value
}

export const RESET_RUNNING_CRAWLER_TASK_ID = (state) => {
    state.running_crawler_task_id = null
}

export const SET_JOB = (state, job) => {
    // state.job = job
    Vue.set(state.job,0, job[0])
}

export const SET_JOB_STATE = (state, job_state) => {
    // console.log("$$$$$=> JOB STATE")
    // console.log(job_state)
    state.job_state = job_state
}

export const SET_FINISHED_JOBS = (state, finished_jobs) => {
    state.finished_jobs = finished_jobs
}

export const SET_LOADING_CRAWLER_EXECUTION = (state, loading_crawler_execution) => {
    state.loading_crawler_execution = loading_crawler_execution
}

export const SET_POLLING_INTERVAL = (state, polling_interval) => {
    state.polling_interval = polling_interval
}

export const DELETING_CRAWLER_LOADING = (state, deleting_crawler_loading) => {
    state.deleting_crawler_loading = deleting_crawler_loading
}

