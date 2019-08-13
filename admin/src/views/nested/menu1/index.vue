<template>
  <div style="padding:30px;" class="config">
    <table>
      <tr>
        <th>配置项</th>
        <th>状态</th>
      </tr>
      <tr>
        <td>auth_required</td>
        <td>
          <el-switch v-model="auth_required"></el-switch>
        </td>
      </tr>
      <tr>
        <td>key</td>
        <td>
          <el-input v-model="key" placeholder="请输入key"></el-input>
        </td>
      </tr>
      <tr>
        <td>origin_number</td>
        <td>
          <el-input v-model="origin_number" placeholder="请输入origin_number"></el-input>
        </td>
      </tr>
    </table>
    <el-button
      type="success"
      icon="el-icon-check"
      @click="onSubmit(auth_required,key,origin_number)"
    >保存</el-button>
  </div>
</template>
<script>
export default {
  inject: ["reload"],
  data() {
    return {
      token: "",
      auth_required: false,
      key: "",
      origin_number: "",
      configURL: this.URL + "/config_manage"
    };
  },
  methods: {
    getConfigData() {
      this.axios({
        url: this.configURL,
        methods: "get",
        headers: {
          Authorization: "JWT " + this.token
        }
      })
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            let res = returnData.data;
            this.auth_required = res.auth_required == 1 ? true : false;
            this.key = res.key;
            this.origin_number = res.origin_number;
          }else if (returnData.success == false && returnData.token == false) {
            this.logout();
            sessionStorage.removeItem("token");
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    onSubmit(auth_required, key, origin_number) {
      let flag = auth_required == true ? 1 : 0;
      if (key == "" || origin_number == "") {
        return this.$message({
          message: "内容不能为空!",
          type: "error"
        });
      }
      let sendData = {
        auth_required: flag,
        key: key,
        origin_number: origin_number
      };
      this.axios
        .post(this.configURL, this.$qs.stringify(sendData), {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            this.$message({
              message: returnData.msg,
              type: "success"
            });
            setTimeout(() => {
              this.reload();
            }, 1500);
          }else if (returnData.success == false && returnData.token == false) {
            this.logout();
            sessionStorage.removeItem("token");
          }else {
            this.$message({
              showClose: true,
              message: returnData.msg,
              type: "error"
            });
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push(`/login?redirect=${this.$route.fullPath}`);
    }
  },
  mounted() {
    this.token = sessionStorage.getItem("token");
    this.getConfigData();
  }
};
</script>
<style scoped>
.config table {
  width: 100%;
  border-collapse: collapse;
}
.config table tr th,
.config table tr td {
  color: #909399;
  width: 50%;
  text-align: left;
  border: 1px solid #ebeef5;
  padding: 15px;
  font-size: 14px;
}
.config table tr th {
  color: #909399;
}
.config table tr td {
  color: #606266;
}
</style>
<style>
.config .el-button--success {
  margin-top: 20px;
  float: right;
}
</style>
