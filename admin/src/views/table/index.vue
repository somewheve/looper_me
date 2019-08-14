<template>
  <div class="symbol">
    <div class="serach">
      <div class="demo-input-suffix">
        <el-input placeholder="请输入代码" v-model="serachValue" @input="search(serachValue)">
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
      </div>
    </div>
    <div class="symbolTab" v-if="tabFlag">
      <div class="leftTab" style="float:left;width:49%">
        <el-table
          :data="leftData.slice((currentPage-1)*pagesize/2,currentPage*pagesize/2)"
          border
          style="width: 100%"
        >
          <el-table-column prop="name" label="名称"></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="success" @click="see(scope.row.name)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div class="rightTab" style="float:right;width:49%">
        <el-table
          :data="rightData.slice((currentPage-1)*pagesize/2,currentPage*pagesize/2)"
          border
          style="width: 100%"
        >
          <el-table-column prop="name" label="名称"></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="success" @click="see(scope.row.name)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <div class="searchTab" v-if="!tabFlag" style="width:49%">
      <el-table
        :data="searchData.slice((currentPage-1)*pagesize,currentPage*pagesize)"
        border
        style="width: 100%"
      >
        <el-table-column prop="name" label="名称"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="see(scope.row.name)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[20, 40, 60, 80, 100]"
      :page-size="pagesize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="searchData.length"
      style="text-align: center;margin: 50px 0;"
    ></el-pagination>
  </div>
</template>
<script>
export default {
  data() {
    return {
      dataDownLoadURL: this.URL + "/data_manage",
      serachValue: "",
      tabFlag: true,
      currentPage: 1,
      pagesize: 20,
      tableData: [],
      searchData: [],
      leftData: [],
      rightData: []
    };
  },
  created() {
    this.getData();
  },
  methods: {
    search(key) {
      this.currentPage = 1;
      key != "" ? (this.tabFlag = false) : (this.tabFlag = true);
      let searchData = this.tableData.filter(item => {
        return item["name"].includes(key);
      });
      this.searchData = searchData;
    },
    //数据分页--->每页多少数据
    handleSizeChange(size) {
      this.pagesize = size;
    },
    //数据分页--->当前页
    handleCurrentChange(currentPage) {
      this.currentPage = currentPage;
    },
    see(symbol) {
      this.$router.push({
        path: "/download/index",
        query: { symbolName: symbol }
      });
    },
    getData() {
      let token = sessionStorage.getItem("token");
      this.axios
        .get(this.dataDownLoadURL, {
          headers: {
            Authorization: "JWT " + token
          }
        })
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            this.tableData = returnData.data;
            this.searchData = returnData.data;
            this.leftData = this.tableData.filter((item, index) => {
              return index % 2 == 0;
            });
            this.rightData = this.tableData.filter((item, index) => {
              return index % 2 != 0;
            });

            let symbolArr = [];
            for (let i in returnData.data) {
              symbolArr.push(returnData.data[i]["name"]);
            }
            sessionStorage.setItem("symbolArr", JSON.stringify(symbolArr));
          }
        })
        .catch(err => {
          let statusCode = err.response.status;
          if (statusCode === 302) {
            setTimeout(() => {
              this.$message({
                message: "登录信息已过期,请重新登录!",
                type: "error"
              });
              this.logout();
              sessionStorage.removeItem("token");
            }, 100);
          }
        });
    },
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push(`/login?redirect=${this.$route.fullPath}`);
    }
  }
};
</script>
<style scoped>
.symbol {
  box-sizing: border-box;
  padding: 10px 30px 0;
}
.symbolTab,
.searchTab {
  margin-top: 20px;
  overflow: hidden;
}
</style>
