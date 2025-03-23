module.exports = {
    apps: [{
        name: "my_x_downloader",
        cwd: "/Users/herbertgao/my_x_downloader",
        script: "./.venv/bin/python",
        args: "src/main.py",
        cron_restart: "*/30 * * * *",
        autorestart: false,
        error_file: "logs/my_x_downloader_error.log",
        out_file: "logs/my_x_downloader_out.log",
        merge_logs: true,
        env: {
            PYTHONPATH: "/Users/herbertgao/my_x_downloader"
        }
    }]
};