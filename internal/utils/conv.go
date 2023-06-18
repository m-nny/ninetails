package utils

import (
	"bytes"
	"encoding/binary"
	"fmt"
)

func ReadFloat32(fourBytes []byte) (float32, error) {
	buf := bytes.NewBuffer(fourBytes)
	var value float32
	if err := binary.Read(buf, binary.LittleEndian, &value); err != nil {
		return 0, err
	}
	return value, nil
}

func ReadFloat32Slice(arr []byte, size int) ([]float32, error) {
	if len(arr) < size*4 {
		return nil, fmt.Errorf("arr have length of at least %d", size*4)
	}
	var values []float32
	for i := 0; i < size; i++ {
		value, err := ReadFloat32(arr[i*4 : i*4+4])
		if err != nil {
			return nil, err
		}
		values = append(values, value)
	}
	return values, nil
}
