<template>
  <div style="padding:30px;">
    <div>
      <el-form :inline="true" :model="formInline" class="demo-form-inline">
        <el-form-item label="配置名">
          <el-input v-model="formInline.configName" placeholder="配置名"></el-input>
        </el-form-item>
        <el-form-item label="配置值">
          <el-input v-model="formInline.configValue" placeholder="配置值"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-plus" @click="onSubmit">添加</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-table :data="tableData" border fit style="width: 100%">
      <el-table-column prop="date" label="配置名"></el-table-column>
      <el-table-column prop="name" label="配置值"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button-group>
            <el-button
              size="mini"
              type="success"
              icon="el-icon-edit"
              @click="edit(scope.$index, scope.row)"
            >编辑</el-button>
            <el-button
              size="mini"
              type="danger"
              icon="el-icon-delete"
              @click="delete(scope.$index, scope.row)"
            >删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
export default {
  data() {
    return {
      configURL: this.URL + "/config_manage",
      formInline: {
        configName: "",
        configValue: ""
      },
      tableData: [{ date: "666", name: "123" }]
    };
  },
  methods: {
    getConfigData() {
      this.axios({
        url: this.configURL,
        methods: "get"
      })
        .then(data => {
          console.log(data);
        })
        .catch(err => {
          console.log(err);
        });
    },
    onSubmit() {},
    edit(){},
    delete(){}
  },
  mounted() {
    // this.getConfigData();
  }
};
</script>
<style scoped>
</style>
