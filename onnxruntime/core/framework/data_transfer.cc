// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

#include "core/framework/data_transfer.h"

namespace onnxruntime {

common::Status IDataTransfer::CopyTensor(const Tensor& src, Tensor& dst) const {
  return CopyTensor(src, dst, 0);
}

bool CPUDataTransfer::CanCopy(const OrtDevice& src_device, const OrtDevice& dst_device) const {
  return src_device.Type() == OrtDevice::CPU && dst_device.Type() == OrtDevice::CPU;
}

common::Status CPUDataTransfer::CopyTensor(const Tensor& src, Tensor& dst, int /*exec_queue_id*/) const {
  const void* src_data = src.DataRaw();
  void* dst_data = dst.MutableDataRaw();
  memcpy(dst_data, src_data, src.Size());
  return Status::OK();
}

};  // namespace onnxruntime
