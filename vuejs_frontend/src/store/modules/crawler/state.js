export default{
    start_url:'',
    other_errors:[],
    crawlers:[],
    loading:false,
    loading_scrapyd:false,
    loading_crawler_execution:false,
    running_crawler:null,
    running_crawler_task_id:null,
    job:[],
    finished_jobs: [],
    job_state:'finished',
    polling_interval: null,
    deleting_crawler_loading: false,
    crawler_details_loading: false,
    crawler_details:{},
    crawler_logfile: ''
}