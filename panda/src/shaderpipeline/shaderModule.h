/**
 * PANDA 3D SOFTWARE
 * Copyright (c) Carnegie Mellon University.  All rights reserved.
 *
 * All use of this software is subject to the terms of the revised BSD
 * license.  You should have received a copy of this license along
 * with this source code in a file named "LICENSE."
 *
 * @file shaderModule.h
 * @author Mitchell Stokes
 * @date 2019-02-16
 */

#ifndef SHADERMODULE_H
#define SHADERMODULE_H

#include "copyOnWriteObject.h"
#include "bamCacheRecord.h"
#include "shaderType.h"

/**
 * Represents a single shader module in some intermediate representation for
 * passing to the driver.  This could contain compiled bytecode, or in some
 * cases, preprocessed source code to be given directly to the driver.
 *
 * This class inherits from CopyOnWriteObject so that modules can safely be
 * shared between multiple Shader objects, with a unique copy automatically
 * being created if the Shader needs to manipulate the module.
 */
class EXPCL_PANDA_SHADERPIPELINE ShaderModule : public CopyOnWriteObject {
PUBLISHED:
  enum class Stage {
    vertex,
    tess_control,
    tess_evaluation,
    geometry,
    fragment,
    compute,
  };

  /**
   * Defines an interface variable.
   */
  struct Variable {
  public:
    int has_location() const { return _location >= 0; }
    int get_location() const { return _location; }

  PUBLISHED:
    const ShaderType *type;
    CPT_InternalName name;

    MAKE_PROPERTY2(location, has_location, get_location);

  public:
    int _location;
  };

public:
  ShaderModule(Stage stage);
  virtual ~ShaderModule();

  INLINE Stage get_stage() const;
  INLINE int get_used_capabilities() const;

  INLINE const Filename &get_source_filename() const;
  INLINE void set_source_filename(const Filename &);

  size_t get_num_inputs() const;
  const Variable &get_input(size_t i) const;
  int find_input(CPT_InternalName name) const;

  size_t get_num_outputs() const;
  const Variable &get_output(size_t i) const;
  int find_output(CPT_InternalName name) const;

  size_t get_num_parameters() const;
  const Variable &get_parameter(size_t i) const;
  int find_parameter(CPT_InternalName name) const;

  typedef pmap<CPT_InternalName, Variable *> VariablesByName;

  virtual bool link_inputs(const ShaderModule *previous);
  virtual void remap_parameter_locations(pmap<int, int> &remap);

PUBLISHED:
  MAKE_PROPERTY(stage, get_stage);
  MAKE_SEQ_PROPERTY(inputs, get_num_inputs, get_input);
  MAKE_SEQ_PROPERTY(outputs, get_num_outputs, get_output);

  virtual std::string get_ir() const=0;

public:
  /**
   * Indicates which features are used by the shader, which can be used by the
   * driver to check whether cross-compilation is possible, or whether certain
   * transformation steps may need to be applied.
   */
  enum Capabilities {
    // GLSL 1.30
    C_integer = 1 << 0,
    C_texture_fetch = 1 << 1, // texelFetch, textureSize, etc.
    C_buffer_texture = 1 << 2,
    C_vertex_id = 1 << 3,
    C_round_even = 1 << 4,

    // GLSL 1.40
    C_instance_id = 1 << 5,

    // GLSL 1.50
    C_geometry_shader = 1 << 6,
    C_primitive_id = 1 << 7,

    // GLSL 3.30 / ARB_shader_bit_encoding
    C_bit_encoding = 1 << 8,

    // GLSL 4.00
    C_double = 1 << 9,
    C_cube_map_array = 1 << 10,
    C_tessellation_shader = 1 << 11,
    C_sample_variables = 1 << 12,
    C_extended_arithmetic = 1 << 13,
    C_texture_query_lod = 1 << 14,

    // GLSL 4.20
    C_image_load_store = 1 << 15,

    // GLSL 4.30
    C_compute_shader = 1 << 16,
    C_texture_query_levels = 1 << 17,

    // GLSL 4.40 / ARB_enhanced_layouts
    C_enhanced_layouts = 1 << 18,

    // GLSL 4.50
    C_derivative_control = 1 << 19,
    C_texture_query_samples = 1 << 20,
  };

  static std::string format_stage(Stage stage);
  static void output_capabilities(std::ostream &out, int capabilities);

  virtual void output(std::ostream &out) const;

  virtual void write_datagram(BamWriter *manager, Datagram &dg) override;

protected:
  void fillin(DatagramIterator &scan, BamReader *manager) override;

protected:
  Stage _stage;
  PT(BamCacheRecord) _record;
  //std::pvector<Filename> _source_files;
  Filename _source_filename;
  //time_t _source_modified = 0;
  int _used_caps = 0;

  typedef pvector<Variable> Variables;
  Variables _inputs;
  Variables _outputs;
  Variables _parameters;

  friend class Shader;

public:
  static TypeHandle get_class_type() {
    return _type_handle;
  }
  static void init_type() {
    TypedWritableReferenceCount::init_type();
    register_type(_type_handle, "ShaderModule",
                  TypedWritableReferenceCount::get_class_type());
  }
  virtual TypeHandle get_type() const override {
    return get_class_type();
  }
  virtual TypeHandle force_init_type() override {
    init_type();
    return get_class_type();
  }

private:
  static TypeHandle _type_handle;
};

INLINE std::ostream &operator << (std::ostream &out, const ShaderModule &module) {
  module.output(out);
  return out;
}

INLINE std::ostream &operator << (std::ostream &out, ShaderModule::Stage stage) {
  return out << ShaderModule::format_stage(stage);
}

#include "shaderModule.I"

#endif