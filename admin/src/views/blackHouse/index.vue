<template>
<div class="ipTab">
  <el-table :data="tableData" border style="width: 100%">
    <el-table-column type="index">
    </el-table-column>
    <el-table-column prop="ip" label="ip地址">
    </el-table-column>
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
  inject:['reload'],
  data() {
    return {
      blacklistURL: this.URL + '/blacklist_manage',
      tableData: []
    }
  },
  methods: {
    getBlackHouseData() {
      this.axios.get(this.blacklistURL).then(data => {
        let returnData=data.data
        if(returnData.success==true){
          this.tableData=returnData.data
        }
      }).catch(err => {
        console.log(err);
      })
    },
    Unsealing(row){
      let sendData={
        'todo':'alive',
        'ip':row.ip
      }
      this.axios.post(this.blacklistURL, this.$qs.stringify(sendData)).then(data => {
        let returnData=data.data
        if(returnData.success==true){
          this.$message({
            message:returnData.msg,
            type: 'success',
            center: true
          });
          setTimeout(()=>{
            this.reload()
          },1500)
        }
      }).catch(err => {
        console.log(err);
      })
    }
  },
  mounted(){
    this.getBlackHouseData()
  }
}
</script>

<style scoped>
.ipTab {
  padding: 20px;
}
</style>
