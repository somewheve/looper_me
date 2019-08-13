<template>
  <div class="ipTab">
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column type="index"></el-table-column>
      <el-table-column prop="ip" label="ip地址"></el-table-column>
      <el-table-column prop="address" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="success" @click="Unsealing(scope.row)">解封</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  inject: ["reload"],
  data() {
    return {
      token:"",
      blacklistURL: this.URL + "/blacklist_manage",
      tableData: []
    };
  },
  methods: {
    getBlackHouseData() {
      this.axios
        .get(this.blacklistURL,{
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            this.tableData = returnData.data;
          }else if (returnData.success == false && returnData.token == false) {
            this.logout();
            sessionStorage.removeItem("token");
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    Unsealing(row) {
      let sendData = {
        todo: "alive",
        ip: row.ip
      };
      this.axios
        .post(this.blacklistURL, this.$qs.stringify(sendData),{
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
          } else if (returnData.success == false && returnData.token == false) {
            this.logout();
            sessionStorage.removeItem("token");
          }else{
             this.$message({
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
    this.getBlackHouseData();
  }
};
</script>

<style scoped>
.ipTab {
  padding: 20px;
}
</style>
